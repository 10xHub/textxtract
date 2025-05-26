"""HTML file handler for text extraction."""

from pathlib import Path
from typing import Optional

from textxtract.core.base import FileTypeHandler
from textxtract.core.exceptions import ExtractionError


class HTMLHandler(FileTypeHandler):
    """Handler for extracting text from HTML files."""

    def extract(self, file_path: Path, config: Optional[dict] = None) -> str:
        try:
            try:
                from bs4 import BeautifulSoup
            except ImportError:
                raise ExtractionError(
                    "beautifulsoup4 package is not installed. Install with 'pip install text-extractor[html]'"
                )
            text = file_path.read_text(encoding=(config or {}).get("encoding", "utf-8"))
            soup = BeautifulSoup(text, "html.parser")
            return soup.get_text()
        except Exception as e:
            raise ExtractionError(f"HTML extraction failed: {e}")

    async def extract_async(
        self, file_path: Path, config: Optional[dict] = None
    ) -> str:
        import asyncio

        return await asyncio.to_thread(self.extract, file_path, config)
