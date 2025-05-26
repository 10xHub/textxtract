"""Comprehensive tests for AsyncTextExtractor using all sample files."""

import pytest
from textxtract.aio import AsyncTextExtractor
from textxtract.core.exceptions import (
    ExtractionError,
    InvalidFileError,
    FileTypeNotSupportedError,
)
from pathlib import Path

TEST_FILES_DIR = Path(__file__).parent / "files"


@pytest.mark.parametrize(
    "filename,should_succeed",
    [
        ("text_file.txt", True),
        ("text_file.text", True),
        ("markdown.md", True),
        ("text_file.pdf", True),
        ("text_file.docx", True),
        ("text_file.doc", True),
        ("text_file.rtf", True),
        ("text.html", True),
        ("text.csv", True),
        ("text.json", True),
        ("text.xml", True),
        ("text_zip.zip", True),
        ("text_file.odt", False),  # Not supported, should fail
    ],
)
@pytest.mark.asyncio
async def test_async_extractor_all_types(filename, should_succeed):
    extractor = AsyncTextExtractor()
    file_path = TEST_FILES_DIR / filename
    file_bytes = file_path.read_bytes()
    try:
        text = await extractor.extract(file_bytes, filename)
        assert should_succeed, f"Extraction should have failed for {filename}"
        assert isinstance(text, (str, list)), "Extracted text should be str or list"
        assert text, "Extracted text should not be empty"
    except FileTypeNotSupportedError:
        assert not should_succeed, (
            f"FileTypeNotSupportedError unexpected for {filename}"
        )
    except (ExtractionError, InvalidFileError):
        assert not should_succeed, (
            f"ExtractionError/InvalidFileError unexpected for {filename}"
        )


@pytest.mark.parametrize(
    "filename,should_succeed",
    [
        ("text_file.txt", True),
        ("text_file.text", True),
        ("markdown.md", True),
        ("text_file.pdf", True),
        ("text_file.docx", True),
        ("text_file.doc", True),
        ("text_file.rtf", True),
        ("text.html", True),
        ("text.csv", True),
        ("text.json", True),
        ("text.xml", True),
        ("text_zip.zip", True),
        ("text_file.odt", False),  # Not supported, should fail
    ],
)
@pytest.mark.asyncio
async def test_async_extractor_from_file_path(filename, should_succeed):
    """Test async extraction directly from file path."""
    extractor = AsyncTextExtractor()
    file_path = TEST_FILES_DIR / filename
    try:
        text = await extractor.extract(file_path)
        assert should_succeed, f"Extraction should have failed for {filename}"
        assert isinstance(text, (str, list)), "Extracted text should be str or list"
        assert text, "Extracted text should not be empty"
    except FileTypeNotSupportedError:
        assert not should_succeed, (
            f"FileTypeNotSupportedError unexpected for {filename}"
        )
    except (ExtractionError, InvalidFileError):
        assert not should_succeed, (
            f"ExtractionError/InvalidFileError unexpected for {filename}"
        )
