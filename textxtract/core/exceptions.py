"""Custom exceptions for textxtract package."""


class ExtractionError(Exception):
    """Raised when a general extraction error occurs."""


class InvalidFileError(ExtractionError):
    """Raised when the file is invalid or unsupported."""


class FileTypeNotSupportedError(ExtractionError):
    """Raised when the file type is not supported."""


class ExtractionTimeoutError(ExtractionError):
    """Raised when extraction exceeds the allowed timeout."""
