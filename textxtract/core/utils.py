"""Utility functions for textxtract package."""

import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Union

# Security limits
DEFAULT_MAX_FILE_SIZE = 100 * 1024 * 1024  # 100MB
DEFAULT_MAX_TEMP_FILES = 1000


@dataclass
class FileInfo:
    """File information data class."""

    filename: str
    size_bytes: int
    size_mb: float
    extension: str
    is_temp: bool = False

    @property
    def size_kb(self) -> float:
        """File size in KB."""
        return round(self.size_bytes / 1024, 2)


def validate_file_size(file_bytes: bytes, max_size: Optional[int] = None) -> None:
    """Validate file size doesn't exceed limits."""
    max_size = max_size or DEFAULT_MAX_FILE_SIZE
    if len(file_bytes) == 0:
        raise ValueError("File is empty (0 bytes)")
    if len(file_bytes) > max_size:
        raise ValueError(
            f"File size ({len(file_bytes):,} bytes) exceeds maximum "
            f"allowed size ({max_size:,} bytes)"
        )


def validate_filename(filename: str) -> None:
    """Validate filename for security issues."""
    if not filename:
        raise ValueError("Filename cannot be empty")

    # Check for null bytes
    if "\x00" in filename:
        raise ValueError("Invalid filename: contains null byte")

    # Check for path traversal attempts
    if ".." in filename:
        raise ValueError("Invalid filename: path traversal detected")

    # Check for absolute paths (both Unix and Windows)
    if filename.startswith("/") or (len(filename) > 1 and filename[1] == ":"):
        raise ValueError("Invalid filename: absolute path not allowed")

    # Check for Windows path separators in suspicious contexts
    if "\\" in filename and (".." in filename or filename.count("\\") > 2):
        raise ValueError("Invalid filename: suspicious path structure")

    # Check filename length
    if len(filename) > 255:
        raise ValueError("Filename too long")


def create_temp_file(
    file_bytes: bytes, filename: str, max_size: Optional[int] = None
) -> Path:
    """Create a temporary file from bytes and return its path with security validation."""
    validate_filename(filename)
    validate_file_size(file_bytes, max_size)

    file_ext = Path(filename).suffix
    with tempfile.NamedTemporaryFile(delete=False, suffix=file_ext) as temp_file:
        temp_file.write(file_bytes)
        temp_path = Path(temp_file.name)

    # Ensure file was created successfully
    if not temp_path.exists():
        raise RuntimeError("Failed to create temporary file")

    return temp_path


def safe_unlink(path: Path, log_errors: bool = True) -> bool:
    """Safely delete a file if it exists, optionally logging errors."""
    try:
        if path.exists():
            path.unlink()
            return True
        return False
    except Exception as e:
        if log_errors:
            import logging

            logger = logging.getLogger("textxtract.utils")
            logger.warning("Failed to delete temporary file %s: %s", path, e)
        return False


def validate_file_extension(filename: str, allowed_extensions: list[str]) -> bool:
    """Check if the file has an allowed extension."""
    return Path(filename).suffix.lower() in allowed_extensions


def get_file_info(
    source: Union[Path, str, bytes], filename: Optional[str] = None
) -> FileInfo:
    """
    Get file information for logging and debugging.

    Args:
        source: File path or file bytes
        filename: Required if source is bytes, optional for file paths

    Returns:
        FileInfo: Data class with file information
    """
    if isinstance(source, bytes):
        if not filename:
            raise ValueError("filename is required when source is bytes")
        return FileInfo(
            filename=filename,
            size_bytes=len(source),
            size_mb=round(len(source) / (1024 * 1024), 2),
            extension=Path(filename).suffix.lower(),
            is_temp=True,
        )
    else:
        # Handle file path
        file_path = Path(source)
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        if not file_path.is_file():
            raise ValueError(f"Path is not a file: {file_path}")

        file_size = file_path.stat().st_size
        return FileInfo(
            filename=filename or file_path.name,
            size_bytes=file_size,
            size_mb=round(file_size / (1024 * 1024), 2),
            extension=file_path.suffix.lower(),
            is_temp=False,
        )
