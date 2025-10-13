"""DOCX file handler for comprehensive text extraction.

This handler extracts text from:
- Document paragraphs
- Tables and cells
- Headers and footers
- Text boxes and shapes
- Footnotes and endnotes (if available)
"""

from pathlib import Path
from typing import Optional
import re

from textxtract.core.base import FileTypeHandler
from textxtract.core.exceptions import ExtractionError


class DOCXHandler(FileTypeHandler):
    """Enhanced handler for comprehensive text extraction from DOCX files.
    
    Extracts text from all document elements including paragraphs, tables,
    headers, footers, text boxes, and footnotes to ensure complete content
    extraction for documents like resumes, reports, and complex layouts.
    """

    def _clean_text(self, text: str) -> str:
        """Clean and normalize extracted text."""
        if not text:
            return ""
        
        # Normalize whitespace
        text = re.sub(r'\s+', ' ', text)
        # Remove excessive dots/periods
        text = re.sub(r'\.{2,}', ' ', text)
        # Clean up spacing around punctuation
        text = re.sub(r'\s+([.!?,:;])', r'\1', text)
        return text.strip()

    def extract(self, file_path: Path, config: Optional[dict] = None) -> str:
        try:
            from docx import Document
            import re

            doc = Document(file_path)
            text_parts = []
            processed_text = set()  # To avoid duplicates
            
            # Extract text from paragraphs
            for paragraph in doc.paragraphs:
                text = paragraph.text.strip()
                if text and text not in processed_text:
                    text_parts.append(text)
                    processed_text.add(text)
            
            # Extract text from tables
            for table in doc.tables:
                table_texts = []
                for row in table.rows:
                    row_text = []
                    for cell in row.cells:
                        # Get text from all paragraphs in the cell
                        cell_paragraphs = []
                        for paragraph in cell.paragraphs:
                            text = paragraph.text.strip()
                            if text and text not in processed_text:
                                cell_paragraphs.append(text)
                                processed_text.add(text)
                        if cell_paragraphs:
                            row_text.append(" ".join(cell_paragraphs))
                    if row_text:
                        table_texts.append(" | ".join(row_text))
                
                # Add table content if any
                if table_texts:
                    text_parts.extend(table_texts)
            
            # Extract text from headers and footers
            for section in doc.sections:
                # Header text
                if section.header:
                    for paragraph in section.header.paragraphs:
                        text = paragraph.text.strip()
                        if text and text not in processed_text:
                            text_parts.append(text)
                            processed_text.add(text)
                
                # Footer text
                if section.footer:
                    for paragraph in section.footer.paragraphs:
                        text = paragraph.text.strip()
                        if text and text not in processed_text:
                            text_parts.append(text)
                            processed_text.add(text)
            
            # Try to extract text from footnotes and endnotes
            try:
                # Extract footnotes
                if hasattr(doc, 'footnotes'):
                    for footnote in doc.footnotes:
                        for paragraph in footnote.paragraphs:
                            text = paragraph.text.strip()
                            if text and text not in processed_text:
                                text_parts.append(f"[Footnote: {text}]")
                                processed_text.add(text)
                
                # Extract endnotes
                if hasattr(doc, 'endnotes'):
                    for endnote in doc.endnotes:
                        for paragraph in endnote.paragraphs:
                            text = paragraph.text.strip()
                            if text and text not in processed_text:
                                text_parts.append(f"[Endnote: {text}]")
                                processed_text.add(text)
            except Exception:
                # If footnotes/endnotes extraction fails, continue
                pass
            
            # Try to extract text from text boxes and shapes using xml parsing
            try:
                from docx.oxml.ns import qn
                
                # Look for drawing elements containing text
                for element in doc.element.body.iter():
                    if element.tag.endswith('}txbxContent'):
                        # Extract text from text boxes
                        for para in element.iter():
                            if para.tag.endswith('}t') and para.text:
                                text = para.text.strip()
                                if text and text not in processed_text:
                                    text_parts.append(f"[TextBox: {text}]")
                                    processed_text.add(text)
            except Exception:
                # If text box extraction fails, continue
                pass
            
            # Clean up and join text
            if text_parts:
                # Clean each part and join with newlines
                cleaned_parts = [self._clean_text(part) for part in text_parts if part.strip()]
                result = "\n".join(cleaned_parts)
                
                # Ensure proper sentence breaks for readability
                result = re.sub(r'([.!?])\s*([A-Z])', r'\1\n\2', result)
                return result.strip()
            
            return ""
            
        except Exception as e:
            raise ExtractionError(f"DOCX extraction failed: {e}")

    async def extract_async(
        self, file_path: Path, config: Optional[dict] = None
    ) -> str:
        import asyncio

        return await asyncio.to_thread(self.extract, file_path, config)
