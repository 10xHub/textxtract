"""Asynchronous text extraction logic with support for file paths and bytes."""

import asyncio
import logging
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Optional, Union

from textxtract.core.base import TextExtractor
from textxtract.core.config import ExtractorConfig
from textxtract.core.utils import create_temp_file, safe_unlink, get_file_info
from textxtract.core.registry import registry
from textxtract.core.exceptions import (
    ExtractionError,
    FileTypeNotSupportedError,
    InvalidFileError,
)

logger = logging.getLogger("textxtract.aio")


class AsyncTextExtractor(TextExtractor):
    """
    Asynchronous text extractor with support for file paths and bytes.

    Provides asynchronous text extraction from various file types.
    Logs debug and info level messages for tracing and diagnostics.
    Uses thread pool for I/O-bound operations.
    """

    def __init__(
        self,
        config: Optional[ExtractorConfig] = None,
        max_workers: Optional[int] = None,
    ):
        self.config = config or ExtractorConfig()
        self._executor = ThreadPoolExecutor(max_workers=max_workers)
        self._closed = False
        logger.debug(
            "AsyncTextExtractor initialized with config: %s",
            self.config.__dict__,
        )

    async def extract(
        self,
        source: Union[Path, str, bytes],
        filename: Optional[str] = None,
        config: Optional[dict] = None,
    ) -> str:
        """
        Extract text asynchronously from file path or bytes using thread pool.

        Args:
            source: File path (Path/str) or file bytes
            filename: Required if source is bytes, optional for file paths
            config: Optional configuration overrides

        Returns:
            str: Extracted text.

        Raises:
            ValueError: If filename is missing when source is bytes
            FileTypeNotSupportedError: If the file extension is not supported.
            ExtractionError: If extraction fails.
            InvalidFileError: If the file is invalid or corrupted.
        """
        if getattr(self, "_closed", False):
            raise RuntimeError("Extractor has been closed")

        # Get file info for logging
        file_info = get_file_info(source, filename)
        logger.debug("Processing file: %s", file_info)

        # Prepare file path (create temp file if needed)
        file_path, temp_path = await self._prepare_file_path_async(
            source, filename, config
        )

        try:
            # Validate file extension
            suffix = file_info.extension
            if not suffix:
                raise FileTypeNotSupportedError(
                    f"File has no extension: {file_info.filename}"
                )

            logger.debug("Detected file suffix: %s", suffix)

            # Get handler
            handler = registry.get_handler(suffix)
            handler_name = handler.__class__.__name__

            logger.info(
                "Using handler %s for file %s (size: %s MB, temp: %s)",
                handler_name,
                file_info.filename,
                file_info.size_mb,
                file_info.is_temp,
            )

            # Extract text asynchronously
            try:
                loop = asyncio.get_running_loop()
                result = await loop.run_in_executor(
                    self._executor,
                    handler.extract,
                    file_path,
                    config or self.config.__dict__,
                )
            except Exception as e:
                logger.error(
                    "Extraction failed for file %s (handler: %s): %s",
                    file_info.filename,
                    handler_name,
                    e,
                )

                # Re-raise custom extraction errors
                if isinstance(e, ExtractionError):
                    raise
                # Wrap known invalid file errors
                if isinstance(e, (ValueError, OSError)):
                    raise InvalidFileError(
                        f"Invalid file: {file_info.filename} (handler: {handler_name}, error: {e})"
                    ) from e
                # Wrap as general extraction error
                raise ExtractionError(
                    f"Extraction failed for file {file_info.filename} using {handler_name}: {e}"
                ) from e

            logger.info(
                "Extraction successful for file %s (extracted %d characters)",
                file_info.filename,
                len(result),
            )
            return result

        finally:
            # Clean up temporary file if created
            if temp_path:
                safe_unlink(temp_path)
                logger.debug("Temporary file %s deleted", temp_path)

    async def _prepare_file_path_async(
        self,
        source: Union[Path, str, bytes],
        filename: Optional[str],
        config: Optional[dict],
    ) -> tuple[Path, Optional[Path]]:
        """
        Prepare file path for extraction asynchronously.

        Returns:
            tuple: (file_path, temp_path_if_created)
        """
        if isinstance(source, bytes):
            # Handle bytes input - create temporary file
            if not filename:
                raise ValueError("filename is required when source is bytes")

            # Run temp file creation in thread pool to avoid blocking
            loop = asyncio.get_running_loop()
            temp_path = await loop.run_in_executor(
                self._executor,
                create_temp_file,
                source,
                filename,
                config and config.get("max_file_size"),
            )
            logger.debug(
                "Temporary file created at %s for filename %s", temp_path, filename
            )
            return temp_path, temp_path
        else:
            # Handle file path input
            file_path = Path(source)
            if not file_path.exists():
                raise InvalidFileError(f"File not found: {file_path}")
            if not file_path.is_file():
                raise InvalidFileError(f"Path is not a file: {file_path}")

            logger.debug("Using existing file: %s", file_path)
            return file_path, None

    def __enter__(self):
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit with cleanup."""
        if hasattr(self, "_executor"):
            self._executor.shutdown(wait=False)
        self._closed = True

    async def __aenter__(self):
        """Async context manager entry."""
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit with cleanup."""
        if hasattr(self, "_executor"):
            self._executor.shutdown(wait=False)
        self._closed = True
