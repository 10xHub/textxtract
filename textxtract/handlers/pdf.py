"""PDF file handler for text extraction."""

from pathlib import Path
from typing import Optional

from textxtract.core.base import FileTypeHandler
from textxtract.core.exceptions import ExtractionError, InvalidFileError


class PDFHandler(FileTypeHandler):
    """Handler for extracting text from PDF files with improved error handling."""

    def extract(self, file_path: Path, config: Optional[dict] = None) -> str:
        try:
            try:
                import fitz  # PyMuPDF
            except ImportError:
                raise ExtractionError(
                    "PyMuPDF package is not installed. Install with 'pip install text-extractor[pdf]'"
                )

            doc = fitz.open(file_path)
            extracted_text = []
            empty_pages = 0

            for page_num, page in enumerate(doc):
                page_text = page.get_text("text").strip()
                if not page_text:
                    empty_pages += 1
                    # Try OCR-like text extraction for images
                    page_text = page.get_text("dict")  # Get structured text
                    if page_text and "blocks" in page_text:
                        # Check if page has images but no text
                        has_images = any(
                            block.get("type") == 1
                            for block in page_text.get("blocks", [])
                        )
                        if has_images:
                            extracted_text.append(
                                f"[Page {page_num + 1}: Contains images but no extractable text]"
                            )
                        else:
                            extracted_text.append(f"[Page {page_num + 1}: Empty page]")
                    else:
                        extracted_text.append(f"[Page {page_num + 1}: Empty page]")
                else:
                    extracted_text.append(page_text)

            doc.close()

            # Only raise error if ALL pages are empty and there's no content at all
            if not any(
                text.strip() and not text.startswith("[Page") for text in extracted_text
            ):
                if empty_pages == len(extracted_text):
                    raise InvalidFileError(
                        f"PDF contains {empty_pages} empty pages with no extractable text. "
                        "This may be a scanned PDF that requires OCR."
                    )

            result = "\n".join(extracted_text)
            return result

        except fitz.FileDataError as e:
            raise InvalidFileError(f"Invalid or corrupted PDF file: {e}")
        except fitz.EmptyFileError:
            raise InvalidFileError("PDF file is empty")
        except Exception as e:
            if isinstance(e, (ExtractionError, InvalidFileError)):
                raise
            raise ExtractionError(f"PDF extraction failed: {e}")

    async def extract_async(
        self, file_path: Path, config: Optional[dict] = None
    ) -> str:
        import asyncio

        return await asyncio.to_thread(self.extract, file_path, config)
