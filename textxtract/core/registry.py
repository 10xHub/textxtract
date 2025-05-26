"""Handler registry for centralized handler management."""

import logging
from typing import Dict, Type, Optional, List
from functools import lru_cache
from pathlib import Path

from textxtract.core.base import FileTypeHandler
from textxtract.core.exceptions import FileTypeNotSupportedError

logger = logging.getLogger("textxtract.registry")


class HandlerRegistry:
    """Central registry for file type handlers with caching and lazy loading."""

    _instance: Optional["HandlerRegistry"] = None
    _handlers: Dict[str, Type[FileTypeHandler]] = {}
    _initialized = False

    def __new__(cls) -> "HandlerRegistry":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if not self._initialized:
            self._load_default_handlers()
            self._initialized = True

    def _load_default_handlers(self):
        """Load default handlers with lazy imports."""
        # Import handlers at runtime to support optional dependencies
        try:
            from textxtract.handlers.pdf import PDFHandler

            self._handlers[".pdf"] = PDFHandler
        except ImportError:
            logger.debug("PDF handler not available - pymupdf not installed")

        try:
            from textxtract.handlers.docx import DOCXHandler

            self._handlers[".docx"] = DOCXHandler
        except ImportError:
            logger.debug("DOCX handler not available - python-docx not installed")

        try:
            from textxtract.handlers.doc import DOCHandler

            self._handlers[".doc"] = DOCHandler
        except ImportError:
            logger.debug("DOC handler not available - antiword not installed")

        # Always available handlers
        from textxtract.handlers.txt import TXTHandler
        from textxtract.handlers.zip import ZIPHandler

        self._handlers[".txt"] = TXTHandler
        self._handlers[".text"] = TXTHandler
        self._handlers[".zip"] = ZIPHandler

        # Optional handlers with graceful fallback
        try:
            from textxtract.handlers.md import MDHandler

            self._handlers[".md"] = MDHandler
        except ImportError:
            logger.debug("MD handler not available - markdown not installed")

        try:
            from textxtract.handlers.rtf import RTFHandler

            self._handlers[".rtf"] = RTFHandler
        except ImportError:
            logger.debug("RTF handler not available - pyrtf-ng not installed")

        try:
            from textxtract.handlers.html import HTMLHandler

            self._handlers[".html"] = HTMLHandler
            self._handlers[".htm"] = HTMLHandler
        except ImportError:
            logger.debug("HTML handler not available - beautifulsoup4 not installed")

        # Standard library handlers
        from textxtract.handlers.csv import CSVHandler
        from textxtract.handlers.json import JSONHandler

        self._handlers[".csv"] = CSVHandler
        self._handlers[".json"] = JSONHandler

        try:
            from textxtract.handlers.xml import XMLHandler

            self._handlers[".xml"] = XMLHandler
        except ImportError:
            logger.debug("XML handler not available - lxml not installed")

    @lru_cache(maxsize=128)
    def get_handler(self, extension: str) -> FileTypeHandler:
        """Get handler instance for file extension with caching."""
        ext = extension.lower()
        handler_cls = self._handlers.get(ext)

        if not handler_cls:
            available = list(self._handlers.keys())
            raise FileTypeNotSupportedError(
                f"Unsupported file extension: {ext}. "
                f"Supported extensions: {', '.join(available)}"
            )

        # Create handler instance (handlers are lightweight and stateless)
        return handler_cls()

    def register_handler(self, extension: str, handler_cls: Type[FileTypeHandler]):
        """Register a custom handler for a file extension."""
        ext = extension.lower()
        if not ext.startswith("."):
            ext = f".{ext}"

        self._handlers[ext] = handler_cls
        # Clear cache when new handlers are registered
        self.get_handler.cache_clear()
        logger.info(
            "Registered custom handler %s for extension %s", handler_cls.__name__, ext
        )

    def get_supported_extensions(self) -> List[str]:
        """Get list of all supported file extensions."""
        return list(self._handlers.keys())

    def is_supported(self, extension: str) -> bool:
        """Check if a file extension is supported."""
        return extension.lower() in self._handlers


# Global registry instance
registry = HandlerRegistry()
