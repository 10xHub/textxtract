"""Synchronous text extraction logic."""

from typing import Optional
from pathlib import Path
import logging

from textxtract.core.base import TextExtractor
from textxtract.core.config import ExtractorConfig
from textxtract.core.utils import create_temp_file, safe_unlink, get_file_info
from textxtract.core.registry import registry

logger = logging.getLogger("textxtract.sync")


class SyncTextExtractor(TextExtractor):
    """
    Synchronous text extractor with improved error handling and resource management.

    Provides synchronous text extraction from various file types.
    Logs debug and info level messages for tracing and diagnostics.
    Supports context manager protocol for proper cleanup.
    """

    def __init__(self, config: Optional[ExtractorConfig] = None):
        self.config = config or ExtractorConfig()
        logger.debug(
            "SyncTextExtractor initialized with config: %s", self.config.__dict__
        )

    def extract(
        self,
        file_bytes: bytes,
        filename: str,
        config: Optional[dict] = None,
    ) -> str:
        """
        Extract text synchronously from file bytes.

        Args:
            file_bytes (bytes): The file content as bytes.
            filename (str): The name of the file (used for extension).
            config (Optional[dict]): Optional configuration overrides.

        Returns:
            str: Extracted text.

        Raises:
            FileTypeNotSupportedError: If the file extension is not supported.
            ExtractionError: If extraction fails.
            InvalidFileError: If the file is invalid or corrupted.
        """
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

            try:
                result = handler.extract(temp_path, config or self.config.__dict__)
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

    def __enter__(self):
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        pass  # No resources to clean up for sync extractor
