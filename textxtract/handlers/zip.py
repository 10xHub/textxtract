"""ZIP file handler for text extraction."""

from pathlib import Path
from typing import Optional, List
import zipfile
import tempfile
import logging

from textxtract.core.base import FileTypeHandler
from textxtract.core.exceptions import ExtractionError

logger = logging.getLogger("textxtract.handlers.zip")


class ZIPHandler(FileTypeHandler):
    """Handler for extracting text from ZIP archives with security checks."""

    MAX_EXTRACT_SIZE = 1024 * 1024 * 1024  # 1GB total
    MAX_FILES = 1000  # Maximum files to process

    def extract(self, file_path: Path, config: Optional[dict] = None) -> List[str]:
        extracted_texts = []
        total_size = 0
        file_count = 0

        try:
            with zipfile.ZipFile(file_path, "r") as zip_file:
                for file_info in zip_file.infolist():
                    if file_info.is_dir():
                        continue

                    # Security checks
                    if file_count >= self.MAX_FILES:
                        logger.warning("Maximum file limit reached in ZIP archive")
                        break

                    # Check for path traversal
                    if self._is_unsafe_path(file_info.filename):
                        logger.warning("Skipping unsafe path: %s", file_info.filename)
                        continue

                    # Check file size
                    if file_info.file_size > 100 * 1024 * 1024:  # 100MB per file
                        logger.warning(
                            "Skipping large file: %s (%d bytes)",
                            file_info.filename,
                            file_info.file_size,
                        )
                        continue

                    total_size += file_info.file_size
                    if total_size > self.MAX_EXTRACT_SIZE:
                        logger.warning("Total extract size limit reached")
                        break

                    file_count += 1

                    try:
                        with zip_file.open(file_info.filename) as source_file:
                            file_bytes = source_file.read()
                            suffix = Path(file_info.filename).suffix.lower()

                            # Use registry to get handler
                            from textxtract.core.registry import registry

                            if registry.is_supported(suffix):
                                handler = registry.get_handler(suffix)
                                with tempfile.NamedTemporaryFile(
                                    delete=False, suffix=suffix
                                ) as temp_file:
                                    temp_file.write(file_bytes)
                                    temp_path = Path(temp_file.name)
                                try:
                                    text = handler.extract(temp_path, config)
                                    extracted_texts.append(text)
                                    logger.debug(
                                        "Extracted text from %s", file_info.filename
                                    )
                                except Exception as e:
                                    logger.warning(
                                        "Failed to extract text from %s: %s",
                                        file_info.filename,
                                        e,
                                    )
                                finally:
                                    temp_path.unlink(missing_ok=True)
                            else:
                                logger.debug(
                                    "Unsupported file type: %s", file_info.filename
                                )

                    except Exception as e:
                        logger.warning(
                            "Error processing file %s: %s", file_info.filename, e
                        )
                        continue

            logger.info(
                "Extracted text from %d files in ZIP archive", len(extracted_texts)
            )
            return extracted_texts

        except Exception as e:
            raise ExtractionError(f"ZIP extraction failed: {e}")

    def _is_unsafe_path(self, path: str) -> bool:
        """Check if a path contains unsafe elements."""
        # Normalize path separators
        normalized = path.replace("\\", "/")

        # Check for path traversal attempts
        if ".." in normalized or normalized.startswith("/"):
            return True

        # Check for absolute paths on Windows
        if len(normalized) > 1 and normalized[1] == ":":
            return True

        return False

    async def extract_async(
        self, file_path: Path, config: Optional[dict] = None
    ) -> List[str]:
        import asyncio

        return await asyncio.to_thread(self.extract, file_path, config)
