"""DOC file handler for text extraction."""

from pathlib import Path
from typing import Optional

from textxtract.core.base import FileTypeHandler
from textxtract.core.exceptions import ExtractionError, InvalidFileError


class DOCHandler(FileTypeHandler):
    """Handler for extracting text from DOC files with fallback options."""

    def extract(self, file_path: Path, config: Optional[dict] = None) -> str:
        # Try antiword first
        try:
            return self._extract_with_antiword(file_path)
        except FileNotFoundError:
            # Try alternative methods if antiword is not available
            return self._extract_with_fallback(file_path, config)
        except Exception as e:
            if isinstance(e, ExtractionError):
                raise
            raise ExtractionError(f"DOC extraction failed: {e}")

    def _extract_with_antiword(self, file_path: Path) -> str:
        """Extract text using antiword command."""
        import subprocess

        try:
            result = subprocess.run(
                ["antiword", str(file_path)],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=True,
                timeout=30,  # Add timeout
            )
            content = result.stdout.decode("utf-8").strip()
            if not content:
                raise ExtractionError("antiword returned empty content")
            return content
        except subprocess.TimeoutExpired:
            raise ExtractionError("antiword extraction timed out")
        except subprocess.CalledProcessError as e:
            error_msg = e.stderr.decode() if e.stderr else str(e)
            # Check if the error is due to missing libreoffice dependency
            if (
                "libreoffice" in error_msg.lower()
                or "no such file or directory" in error_msg.lower()
            ):
                # Trigger fallback by raising FileNotFoundError
                raise FileNotFoundError(
                    "antiword requires libreoffice which is not available"
                )
            raise ExtractionError(f"antiword extraction failed: {error_msg}")

    def _extract_with_fallback(
        self,
        file_path: Path,
        config: Optional[dict] = None,
    ) -> str:
        """Fallback extraction methods when antiword is not available."""

        # Try python-docx (works for some DOC files)
        try:
            from docx import Document

            doc = Document(file_path)
            text = "\n".join(paragraph.text for paragraph in doc.paragraphs)
            if text.strip():
                return text
        except Exception:
            pass  # Silent fail, try next method

        # Try reading as binary and looking for text patterns
        try:
            with open(file_path, "rb") as f:
                content = f.read()

            # Simple heuristic: look for readable text in the binary
            text_content = []
            current_text = []

            for byte in content:
                if 32 <= byte <= 126:  # Printable ASCII
                    current_text.append(chr(byte))
                else:
                    if len(current_text) > 3:  # Minimum word length
                        text_content.append("".join(current_text))
                    current_text = []

            if current_text and len(current_text) > 3:
                text_content.append("".join(current_text))

            result = " ".join(text_content)
            if result.strip():
                return f"[Extracted using fallback method - may contain formatting artifacts]\n{result}"

        except Exception:
            pass

        # If all methods fail
        raise ExtractionError(
            "DOC extraction failed. Please install 'antiword' command for better DOC support: "
            "sudo apt-get install antiword (Ubuntu/Debian) or brew install antiword (macOS)"
        )

    async def extract_async(
        self, file_path: Path, config: Optional[dict] = None
    ) -> str:
        import asyncio

        return await asyncio.to_thread(self.extract, file_path, config)
