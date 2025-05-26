"""DOCX file handler for text extraction."""

from pathlib import Path
from typing import Optional

from textxtract.core.base import FileTypeHandler
from textxtract.core.exceptions import ExtractionError, InvalidFileError


class DOCXHandler(FileTypeHandler):
    """Handler for extracting text from DOCX files."""

    def extract(self, file_path: Path, config: Optional[dict] = None) -> str:
        try:
            from docx import Document

            doc = Document(file_path)
            return "\n".join(paragraph.text for paragraph in doc.paragraphs)
        except Exception as e:
            raise ExtractionError(f"DOCX extraction failed: {e}")

    async def extract_async(
        self, file_path: Path, config: Optional[dict] = None
    ) -> str:
        import asyncio

        return await asyncio.to_thread(self.extract, file_path, config)
