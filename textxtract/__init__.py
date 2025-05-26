"""Text Extractor package - Professional text extraction from multiple file formats."""

from textxtract.sync.extractor import SyncTextExtractor
from textxtract.aio.extractor import AsyncTextExtractor

__version__ = "0.2.0"
__all__ = ["SyncTextExtractor", "AsyncTextExtractor"]
