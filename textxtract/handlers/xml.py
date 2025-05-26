"""XML file handler for text extraction."""

from pathlib import Path
from typing import Optional

from textxtract.core.base import FileTypeHandler
from textxtract.core.exceptions import ExtractionError


class XMLHandler(FileTypeHandler):
    """Handler for extracting text from XML files."""

    def extract(self, file_path: Path, config: Optional[dict] = None) -> str:
        try:
            try:
                from lxml import etree
            except ImportError:
                raise ExtractionError(
                    "lxml package is not installed. Install with 'pip install text-extractor[xml]'"
                )
            encoding = (config or {}).get("encoding", "utf-8")
            with open(file_path, "r", encoding=encoding) as f:
                tree = etree.parse(f)
                return " ".join(tree.xpath("//text()"))
        except Exception as e:
            raise ExtractionError(f"XML extraction failed: {e}")

    async def extract_async(
        self, file_path: Path, config: Optional[dict] = None
    ) -> str:
        import asyncio

        return await asyncio.to_thread(self.extract, file_path, config)
