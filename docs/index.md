# TextXtract

**TextXtract** is a professional, extensible Python package for extracting text from multiple file formats with both synchronous and asynchronous support.

## 🚀 Key Features

- **Dual Input Support**: Works with file paths or raw bytes
- **Sync & Async APIs**: Choose the right approach for your use case
- **Multiple Formats**: PDF, DOCX, DOC, TXT, ZIP, Markdown, RTF, HTML, CSV, JSON, XML
- **Optional Dependencies**: Install only what you need
- **Robust Error Handling**: Comprehensive exception hierarchy
- **Professional Logging**: Detailed debug and info level logging
- **Thread-Safe**: Async operations use thread pools for I/O-bound tasks
- **Context Manager Support**: Automatic resource cleanup

## 📋 Quick Example

### Synchronous Extraction

```python
from textxtract import SyncTextExtractor

extractor = SyncTextExtractor()

# From file path
text = extractor.extract("document.pdf")

# From bytes (filename required for type detection)
with open("document.pdf", "rb") as f:
    file_bytes = f.read()
text = extractor.extract(file_bytes, "document.pdf")
```

### Asynchronous Extraction

```python
from textxtract import AsyncTextExtractor
import asyncio

async def extract_text():
    extractor = AsyncTextExtractor()
    
    # From file path
    text = await extractor.extract("document.pdf")
    
    # From bytes
    with open("document.pdf", "rb") as f:
        file_bytes = f.read()
    text = await extractor.extract(file_bytes, "document.pdf")
    
    return text

text = asyncio.run(extract_text())
```

## 📚 Documentation

- **[Installation](installation.md)** - Get started quickly
- **[Usage Guide](usage.md)** - Comprehensive usage examples
- **[API Reference](api.md)** - Complete API documentation
- **[Testing](testing.md)** - Running tests and validation
- **[Contributing](contributing.md)** - Help improve the project
- **[Changelog](changelog.md)** - Version history and updates

## 🔧 Supported File Types

| Format | Extension | Dependencies | Handler |
|--------|-----------|--------------|---------|
| Text | `.txt`, `.text` | Built-in | stdlib |
| Markdown | `.md` | `pip install textxtract[md]` | markdown |
| PDF | `.pdf` | `pip install textxtract[pdf]` | PyMuPDF |
| Word | `.docx` | `pip install textxtract[docx]` | python-docx |
| Word Legacy | `.doc` | `pip install textxtract[doc]` | antiword |
| Rich Text | `.rtf` | `pip install textxtract[rtf]` | striprtf |
| HTML | `.html`, `.htm` | `pip install textxtract[html]` | beautifulsoup4 |
| CSV | `.csv` | Built-in | stdlib |
| JSON | `.json` | Built-in | stdlib |
| XML | `.xml` | `pip install textxtract[xml]` | lxml |
| ZIP Archives | `.zip` | Built-in | stdlib |

## 🛡️ Error Handling

Text Extractor provides comprehensive error handling with custom exceptions:

```python
from textxtract import SyncTextExtractor
from textxtract.core.exceptions import (
    FileTypeNotSupportedError,
    InvalidFileError,
    ExtractionError
)

extractor = SyncTextExtractor()

try:
    text = extractor.extract("document.pdf")
except FileTypeNotSupportedError:
    print("File type not supported")
except InvalidFileError:
    print("File is corrupted or invalid")
except ExtractionError:
    print("Extraction failed")
```

## 🎯 Why Choose Text Extractor?

- **Production Ready**: Robust error handling and logging
- **Flexible**: Support for both file paths and bytes
- **Performant**: Async support for concurrent processing
- **Lightweight**: Optional dependencies keep it minimal
- **Well Tested**: Comprehensive test suite
- **Well Documented**: Clear examples and API docs

## 🚀 Get Started

```bash
pip install textxtract
```

Ready to extract text from your files? Check out our [Installation Guide](installation.md) and [Usage Examples](usage.md).