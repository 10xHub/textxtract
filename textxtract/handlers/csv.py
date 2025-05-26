"""CSV file handler for text extraction."""

from pathlib import Path
from typing import Optional
import csv

from textxtract.core.base import FileTypeHandler
from textxtract.core.exceptions import ExtractionError


class CSVHandler(FileTypeHandler):
    """Handler for extracting text from CSV files."""

    def extract(self, file_path: Path, config: Optional[dict] = None) -> str:
        try:
            encoding = (config or {}).get("encoding", "utf-8")
            with open(file_path, "r", encoding=encoding, newline="") as f:
                reader = csv.reader(f)
                return "\n".join([", ".join(row) for row in reader])
        except Exception as e:
            raise ExtractionError(f"CSV extraction failed: {e}")

    async def extract_async(
        self, file_path: Path, config: Optional[dict] = None
    ) -> str:
        import asyncio

        return await asyncio.to_thread(self.extract, file_path, config)
