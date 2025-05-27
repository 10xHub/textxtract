"""Text Extractor package - Professional text extraction from multiple file formats."""

from textxtract.sync.extractor import SyncTextExtractor
from textxtract.aio.extractor import AsyncTextExtractor
from textxtract.core.config import ExtractorConfig

__version__ = "0.2.2"
__all__ = [
    "SyncTextExtractor",
    "AsyncTextExtractor",
    "ExtractorConfig",
]
