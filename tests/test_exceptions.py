"""Unit tests for custom exceptions."""

from textxtract.core.exceptions import (
    ExtractionError,
    InvalidFileError,
    FileTypeNotSupportedError,
    ExtractionTimeoutError,
)


def test_extraction_error():
    e = ExtractionError("error")
    assert str(e) == "error"


def test_invalid_file_error():
    e = InvalidFileError("invalid")
    assert str(e) == "invalid"


def test_file_type_not_supported_error():
    e = FileTypeNotSupportedError("not supported")
    assert str(e) == "not supported"


def test_extraction_timeout_error():
    e = ExtractionTimeoutError("timeout")
    assert str(e) == "timeout"
