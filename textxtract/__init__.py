"""Text Extractor package root."""

from textxtract.sync.extractor import SyncTextExtractor
from textxtract.aio.extractor import AsyncTextExtractor

__all__ = ["SyncTextExtractor", "AsyncTextExtractor"]
