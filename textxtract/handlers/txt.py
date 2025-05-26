"""TXT file handler for text extraction."""

from pathlib import Path
from typing import Optional

from textxtract.core.base import FileTypeHandler
from textxtract.core.exceptions import ExtractionError


class TXTHandler(FileTypeHandler):
    """Handler for extracting text from TXT files."""

    def extract(self, file_path: Path, config: Optional[dict] = None) -> str:
        encoding = (config or {}).get("encoding", "utf-8")
        try:
            return file_path.read_text(encoding=encoding)
        except Exception as e:
            raise ExtractionError(f"TXT extraction failed: {e}")

    async def extract_async(
        self, file_path: Path, config: Optional[dict] = None
    ) -> str:
        import asyncio

        return await asyncio.to_thread(self.extract, file_path, config)
