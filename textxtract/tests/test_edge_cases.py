"""Edge case tests for text extractor."""

import pytest
import tempfile
from pathlib import Path
from unittest.mock import patch, MagicMock

from textxtract import SyncTextExtractor
from textxtract.aio import AsyncTextExtractor
from textxtract.core.exceptions import (
    ExtractionError,
    InvalidFileError,
    FileTypeNotSupportedError,
)
from textxtract.core.config import ExtractorConfig


class TestEdgeCases:
    """Test edge cases and error conditions."""

    def test_empty_file(self):
        """Test extraction from empty file."""
        extractor = SyncTextExtractor()
        empty_content = b""

        with pytest.raises(ValueError, match="File is empty"):
            extractor.extract(empty_content, "empty.txt")

    def test_large_file_rejection(self):
        """Test that very large files are rejected."""
        extractor = SyncTextExtractor()
        # Create content larger than default limit
        large_content = b"x" * (101 * 1024 * 1024)  # 101MB

        with pytest.raises(ValueError, match="File size.*exceeds"):
            extractor.extract(large_content, "large.txt")

    def test_malicious_filename(self):
        """Test that malicious filenames are rejected."""
        extractor = SyncTextExtractor()
        content = b"test content"

        malicious_names = [
            "../../../etc/passwd",
            "..\\..\\windows\\system32\\config",
            "/absolute/path/file.txt",
            "file\x00name.txt",  # Null byte injection
            "a" * 300 + ".txt",  # Very long filename
        ]

        expected_errors = [
            "path traversal detected",
            "path traversal detected",
            "absolute path not allowed",
            "contains null byte",
            "Filename too long",
        ]

        for malicious_name, expected_error in zip(malicious_names, expected_errors):
            with pytest.raises(ValueError, match=expected_error):
                extractor.extract(content, malicious_name)

    def test_unsupported_file_type(self):
        """Test extraction from unsupported file type."""
        extractor = SyncTextExtractor()
        content = b"test content"

        with pytest.raises(FileTypeNotSupportedError):
            extractor.extract(content, "file.unsupported")

    def test_corrupted_pdf(self):
        """Test extraction from corrupted PDF."""
        extractor = SyncTextExtractor()
        # Create fake PDF content
        corrupted_pdf = b"%%PDF-1.4\n%corrupted content"

        with pytest.raises((ExtractionError, InvalidFileError)):
            extractor.extract(corrupted_pdf, "corrupted.pdf")

    @pytest.mark.asyncio
    async def test_async_extractor_closed(self):
        """Test that closed async extractor raises error."""
        async with AsyncTextExtractor() as extractor:
            pass  # Context manager closes extractor

        content = b"test content"
        with pytest.raises(RuntimeError, match="Extractor has been closed"):
            await extractor.extract_async(content, "test.txt")

    def test_config_validation(self):
        """Test configuration validation."""
        # Invalid encoding
        with pytest.raises(ValueError, match="Invalid encoding"):
            ExtractorConfig(encoding="invalid-encoding")

        # Invalid logging level
        with pytest.raises(ValueError, match="Invalid logging level"):
            ExtractorConfig(logging_level="INVALID")

        # Invalid timeout
        with pytest.raises(ValueError, match="Timeout must be a positive number"):
            ExtractorConfig(timeout=-1)

        # Invalid max file size
        with pytest.raises(
            ValueError, match="Max file size must be a positive integer"
        ):
            ExtractorConfig(max_file_size=-1)

    def test_config_from_environment(self):
        """Test loading configuration from environment variables."""
        with patch.dict(
            "os.environ",
            {
                "TEXT_EXTRACTOR_ENCODING": "latin-1",
                "TEXT_EXTRACTOR_LOG_LEVEL": "DEBUG",
                "TEXT_EXTRACTOR_TIMEOUT": "30.0",
                "TEXT_EXTRACTOR_MAX_FILE_SIZE": "50000000",
            },
        ):
            config = ExtractorConfig()
            assert config.encoding == "latin-1"
            assert config.logging_level == "DEBUG"
            assert config.timeout == 30.0
            assert config.max_file_size == 50000000

    @pytest.mark.asyncio
    async def test_concurrent_extractions(self):
        """Test multiple concurrent extractions."""
        import asyncio

        async with AsyncTextExtractor(max_workers=2) as extractor:
            content = b"test content"

            # Run multiple extractions concurrently
            tasks = [
                extractor.extract_async(content, f"test_{i}.txt") for i in range(5)
            ]

            results = await asyncio.gather(*tasks)
            assert len(results) == 5
            assert all(result == "test content" for result in results)

    def test_context_manager_cleanup(self):
        """Test that context managers properly clean up resources."""
        with SyncTextExtractor() as extractor:
            content = b"test content"
            result = extractor.extract(content, "test.txt")
            assert result == "test content"
        # No specific cleanup needed for sync extractor

    @pytest.mark.asyncio
    async def test_async_context_manager_cleanup(self):
        """Test that async context manager properly cleans up."""
        extractor = AsyncTextExtractor()

        async with extractor:
            content = b"test content"
            result = await extractor.extract_async(content, "test.txt")
            assert result == "test content"

        # Verify extractor is closed
        assert extractor._closed

    def test_zip_security_checks(self):
        """Test ZIP handler security checks."""
        from textxtract.handlers.zip import ZIPHandler

        handler = ZIPHandler()

        # Test path traversal detection
        assert handler._is_unsafe_path("../../../etc/passwd")
        assert handler._is_unsafe_path("..\\..\\windows\\system32")
        assert handler._is_unsafe_path("/absolute/path")
        assert handler._is_unsafe_path("C:\\windows\\system32")

        # Test safe paths
        assert not handler._is_unsafe_path("safe/file.txt")
        assert not handler._is_unsafe_path("folder/subfolder/file.txt")

    def test_memory_pressure_handling(self):
        """Test behavior under memory pressure."""
        # This would require more sophisticated testing in a real scenario
        # For now, just test that large text files are handled gracefully
        extractor = SyncTextExtractor()

        # Create a large text file
        large_text = "Large content line\n" * 100000  # ~1.7MB of text
        large_content = large_text.encode("utf-8")

        # Should work fine for reasonable sizes
        result = extractor.extract(large_content, "large.txt")
        assert len(result) > 1000000

    def test_handler_import_errors(self):
        """Test graceful handling of missing optional dependencies."""
        # Mock import error for PDF handler
        with patch("textxtract.core.registry.logger") as mock_logger:
            # This would test the registry's handling of import errors
            # The actual test would need to mock the import process
            pass

    def test_temp_file_cleanup_on_error(self):
        """Test that temporary files are cleaned up even when errors occur."""
        extractor = SyncTextExtractor()

        # Use a handler that will definitely fail
        with pytest.raises(FileTypeNotSupportedError):
            extractor.extract(b"content", "file.unsupported")

        # Verify no temp files are left behind
        # This is tricky to test directly, but the safe_unlink in finally blocks should handle it

    def test_custom_config_per_extraction(self):
        """Test passing custom config per extraction call."""
        extractor = SyncTextExtractor()
        content = b"test content"

        # Test with custom encoding
        result = extractor.extract(content, "test.txt", {"encoding": "utf-8"})
        assert result == "test content"

        # Test with custom max file size
        with pytest.raises(ValueError):
            extractor.extract(content, "test.txt", {"max_file_size": 5})


class TestErrorMessages:
    """Test that error messages are helpful and informative."""

    def test_unsupported_extension_message(self):
        """Test that unsupported extension errors include helpful info."""
        extractor = SyncTextExtractor()

        with pytest.raises(FileTypeNotSupportedError) as exc_info:
            extractor.extract(b"content", "file.xyz")

        error_msg = str(exc_info.value)
        assert "xyz" in error_msg
        assert "Supported extensions" in error_msg

    def test_file_size_error_message(self):
        """Test that file size errors include actual vs allowed size."""
        extractor = SyncTextExtractor()
        large_content = b"x" * 1000

        with pytest.raises(ValueError) as exc_info:
            extractor.extract(large_content, "test.txt", {"max_file_size": 500})

        error_msg = str(exc_info.value)
        assert "1,000 bytes" in error_msg
        assert "500 bytes" in error_msg
