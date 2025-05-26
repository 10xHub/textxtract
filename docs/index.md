# TextXtract

**TextXtract** is a robust, professional Python library for extracting text from a wide range of document formats—synchronously or asynchronously—with a focus on extensibility, security, and performance.

- **Supported formats:** PDF, DOCX, DOC, TXT, ZIP, Markdown, RTF, HTML, CSV, JSON, XML, and more.
- **Features:** Modular handler system, optional dependencies, strong error handling, logging, async support, and easy extensibility.

## Features

- Synchronous and asynchronous APIs
- Modular, extensible file type handlers
- Optional dependencies for lightweight installs
- Professional error handling and logging
- Easy to add new file types
- Comprehensive test suite

## Quick Example

```python
from textxtract.sync.extractor import SyncTextExtractor
extractor = SyncTextExtractor()
text = extractor.extract(file_bytes, filename)

from textxtract.aio.extractor import AsyncTextExtractor
import asyncio
async_extractor = AsyncTextExtractor()
text = asyncio.run(async_extractor.extract_async(file_bytes, filename))
```

## Documentation
- [Architecture Plan](architecture.md)
- [Installation](installation.md)
- [Usage](usage.md)
- [Testing](testing.md)
- [API Reference](api.md)
- [Contributing](contributing.md)
- [Changelog](changelog.md)