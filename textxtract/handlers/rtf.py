"""RTF file handler for text extraction."""

from pathlib import Path
from typing import Optional

from textxtract.core.base import FileTypeHandler
from textxtract.core.exceptions import ExtractionError


class RTFHandler(FileTypeHandler):
    """Handler for extracting text from RTF files."""

    def extract(self, file_path: Path, config: Optional[dict] = None) -> str:
        try:
            try:
                from striprtf.striprtf import rtf_to_text
            except ImportError:
                raise ExtractionError(
                    "striprtf package is not installed. Install with 'pip install text-extractor[rtf]'"
                )

            with open(
                file_path, "r", encoding=(config or {}).get("encoding", "utf-8")
            ) as f:
                rtf_content = f.read()
                return rtf_to_text(rtf_content)
        except Exception as e:
            raise ExtractionError(f"RTF extraction failed: {e}")

    async def extract_async(
        self, file_path: Path, config: Optional[dict] = None
    ) -> str:
        import asyncio

        return await asyncio.to_thread(self.extract, file_path, config)
