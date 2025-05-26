"""Text Extractor package - Professional text extraction from multiple file formats."""

from textxtract.sync.extractor import SyncTextExtractor
from textxtract.aio.extractor import AsyncTextExtractor
from textxtract.core import config
from textxtract.core import exceptions

__version__ = "0.2.0"
__all__ = ["SyncTextExtractor", "AsyncTextExtractor", "config", "exceptions"]
