"""Markdown (.md) file handler for text extraction."""

from pathlib import Path
from typing import Optional

from textxtract.core.base import FileTypeHandler
from textxtract.core.exceptions import ExtractionError


class MDHandler(FileTypeHandler):
    """Handler for extracting text from Markdown files."""

    def extract(self, file_path: Path, config: Optional[dict] = None) -> str:
        try:
            try:
                import markdown
            except ImportError:
                raise ExtractionError(
                    "markdown package is not installed. Install with 'pip install text-extractor[md]'"
                )
            text = file_path.read_text(encoding=(config or {}).get("encoding", "utf-8"))
            # Optionally, convert markdown to plain text (strip HTML)
            html = markdown.markdown(text)
            # Remove HTML tags (best effort, fallback to raw text)
            try:
                from bs4 import BeautifulSoup

                soup = BeautifulSoup(html, "html.parser")
                return soup.get_text()
            except ImportError:
                return text
        except Exception as e:
            raise ExtractionError(f"MD extraction failed: {e}")

    async def extract_async(
        self, file_path: Path, config: Optional[dict] = None
    ) -> str:
        import asyncio

        return await asyncio.to_thread(self.extract, file_path, config)
