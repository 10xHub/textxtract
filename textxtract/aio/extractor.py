"""Asynchronous text extraction logic."""

from typing import Optional
from pathlib import Path
import asyncio
import atexit
from concurrent.futures import ThreadPoolExecutor

from textxtract.core.base import TextExtractor
from textxtract.core.config import ExtractorConfig
from textxtract.core.utils import create_temp_file, safe_unlink, get_file_info
from textxtract.core.registry import registry

import logging

logger = logging.getLogger("textxtract.aio")


class AsyncTextExtractor(TextExtractor):
    """
    Asynchronous text extractor with proper resource management.

    Provides asynchronous text extraction from various file types.
    Logs debug and info level messages for tracing and diagnostics.
    Supports context manager protocol for proper cleanup.
    """

    def __init__(
        self,
        config: Optional[ExtractorConfig] = None,
        max_workers: Optional[int] = None,
    ):
        self.config = config or ExtractorConfig()
        self._executor = ThreadPoolExecutor(max_workers=max_workers)
        self._closed = False

        # Register cleanup on exit
        atexit.register(self._cleanup)

        logger.debug(
            "AsyncTextExtractor initialized with config: %s, max_workers: %s",
            self.config.__dict__,
            max_workers,
        )

    def extract(
        self, file_bytes: bytes, filename: str, config: Optional[dict] = None
    ) -> str:
        """
        Sync interface for compatibility; delegates to async extract.

        Raises:
            NotImplementedError: Always, as async extractor requires async usage.
        """
        raise NotImplementedError(
            "Use extract_async() for asynchronous extraction or use SyncTextExtractor"
        )

    async def extract_async(
        self, file_bytes: bytes, filename: str, config: Optional[dict] = None
    ) -> str:
        """
        Extract text asynchronously from file bytes using a thread pool.

        Args:
            file_bytes (bytes): The file content as bytes.
            filename (str): The name of the file (used for extension).
            config (Optional[dict]): Optional configuration overrides.

        Returns:
            str: Extracted text.

        Raises:
            FileTypeNotSupportedError: If the file extension is not supported.
            ExtractionError: If extraction fails.
            RuntimeError: If extractor is closed.
        """
        if self._closed:
            raise RuntimeError("Extractor has been closed")

        file_info = get_file_info(file_bytes, filename)
        temp_path = create_temp_file(
            file_bytes, filename, config and config.get("max_file_size")
        )

        logger.debug(
            "Temporary file created at %s for file info: %s", temp_path, file_info
        )

        try:
            suffix = Path(filename).suffix.lower()
            logger.debug("Detected file suffix: %s", suffix)

            handler = registry.get_handler(suffix)
            handler_name = handler.__class__.__name__

            logger.info(
                "Using handler %s for file %s (size: %s MB)",
                handler_name,
                filename,
                file_info["size_mb"],
            )

            loop = asyncio.get_running_loop()
            try:
                # Offload sync handler to thread pool for I/O-bound tasks
                result = await loop.run_in_executor(
                    self._executor,
                    handler.extract,
                    temp_path,
                    config or self.config.__dict__,
                )
            except Exception as e:
                from textxtract.core.exceptions import (
                    ExtractionError,
                    InvalidFileError,
                )

                logger.error(
                    "Extraction failed for file %s (handler: %s): %s",
                    filename,
                    handler_name,
                    e,
                )

                # If it's already a custom extraction error, re-raise
                if isinstance(e, ExtractionError):
                    raise
                # If it's a known invalid file error, wrap it
                if isinstance(e, (ValueError, OSError)):
                    raise InvalidFileError(
                        f"Invalid file: {filename} (handler: {handler_name}, error: {e})"
                    ) from e
                # Otherwise, wrap as general extraction error
                raise ExtractionError(
                    f"Extraction failed for file {filename} using {handler_name}: {e}"
                ) from e

            logger.info(
                "Extraction successful for file %s (extracted %d characters)",
                filename,
                len(result),
            )
            return result
        finally:
            safe_unlink(temp_path)
            logger.debug("Temporary file %s deleted", temp_path)

    def close(self):
        """Close the extractor and clean up resources."""
        if not self._closed:
            self._cleanup()
            self._closed = True

    def _cleanup(self):
        """Internal cleanup method."""
        if hasattr(self, "_executor") and self._executor:
            try:
                self._executor.shutdown(wait=True, cancel_futures=True)
                logger.debug("ThreadPoolExecutor shut down successfully")
            except Exception as e:
                logger.warning("Error shutting down ThreadPoolExecutor: %s", e)

    def __enter__(self):
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()

    async def __aenter__(self):
        """Async context manager entry."""
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        self.close()

    def __del__(self):
        """Destructor to ensure cleanup."""
        if not self._closed:
            self._cleanup()
