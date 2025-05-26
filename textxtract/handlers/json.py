"""JSON file handler for text extraction."""

from pathlib import Path
from typing import Optional
import json

from textxtract.core.base import FileTypeHandler
from textxtract.core.exceptions import ExtractionError


class JSONHandler(FileTypeHandler):
    """Handler for extracting text from JSON files."""

    def extract(self, file_path: Path, config: Optional[dict] = None) -> str:
        try:
            encoding = (config or {}).get("encoding", "utf-8")
            with open(file_path, "r", encoding=encoding) as f:
                data = json.load(f)
                # Pretty print JSON as text
                return json.dumps(data, indent=2, ensure_ascii=False)
        except Exception as e:
            raise ExtractionError(f"JSON extraction failed: {e}")

    async def extract_async(
        self, file_path: Path, config: Optional[dict] = None
    ) -> str:
        import asyncio

        return await asyncio.to_thread(self.extract, file_path, config)
