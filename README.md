# TextXtract

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![PyPI version](https://badge.fury.io/py/textxtract.svg)](https://badge.fury.io/py/textxtract)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Tests](https://github.com/10XScale-in/textxtract/workflows/Tests/badge.svg)](https://github.com/10XScale-in/textxtract/actions)

A professional, extensible Python package for extracting text from multiple file formats with both synchronous and asynchronous support.

## 🚀 Features

- **🔄 Dual Input Support**: Works with file paths or raw bytes
- **⚡ Sync & Async APIs**: Choose the right approach for your use case  
- **📁 Multiple Formats**: PDF, DOCX, DOC, TXT, ZIP, Markdown, RTF, HTML, CSV, JSON, XML
- **🎯 Optional Dependencies**: Install only what you need
- **🛡️ Robust Error Handling**: Comprehensive exception hierarchy
- **📊 Professional Logging**: Detailed debug and info level logging
- **🔒 Thread-Safe**: Async operations use thread pools for I/O-bound tasks
- **🧹 Context Manager Support**: Automatic resource cleanup

## Documentation
For complete documentation, including installation instructions, usage examples, and API reference, please visit our [documentation site](https://10xhub.github.io/textxtract/).

## 📦 Installation

### Basic Installation
```bash
pip install textxtract
```

### Install with File Type Support
```bash
# Install support for specific formats
pip install textxtract[pdf]          # PDF support
pip install textxtract[docx]         # Word documents
pip install textxtract[all]          # All supported formats

# Multiple formats
pip install textxtract[pdf,docx,html]
```

## 🏃 Quick Start

### Synchronous Extraction

```python
from textxtract import SyncTextExtractor

extractor = SyncTextExtractor()

# Extract from file path
text = extractor.extract("document.pdf")
print(text)

# Extract from bytes (filename required for type detection)
with open("document.pdf", "rb") as f:
    file_bytes = f.read()
text = extractor.extract(file_bytes, "document.pdf")
print(text)
```

### Asynchronous Extraction

```python
from textxtract import AsyncTextExtractor
import asyncio

async def extract_text():
    extractor = AsyncTextExtractor()
    
    # Extract from file path
    text = await extractor.extract("document.pdf")
    return text

# Run async extraction
text = asyncio.run(extract_text())
print(text)
```

### Context Manager Usage

```python
# Automatic resource cleanup
with SyncTextExtractor() as extractor:
    text = extractor.extract("document.pdf")

# Async context manager
async with AsyncTextExtractor() as extractor:
    text = await extractor.extract("document.pdf")
```

## 📋 Supported File Types

| Format | Extensions | Dependencies | Installation |
|--------|------------|--------------|--------------|
| **Text** | `.txt`, `.text` | Built-in | `pip install textxtract` |
| **Markdown** | `.md` | Optional | `pip install textxtract[md]` |
| **PDF** | `.pdf` | Optional | `pip install textxtract[pdf]` |
| **Word** | `.docx` | Optional | `pip install textxtract[docx]` |
| **Word Legacy** | `.doc` | Optional | `pip install textxtract[doc]` |
| **Rich Text** | `.rtf` | Optional | `pip install textxtract[rtf]` |
| **HTML** | `.html`, `.htm` | Optional | `pip install textxtract[html]` |
| **CSV** | `.csv` | Built-in | `pip install textxtract` |
| **JSON** | `.json` | Built-in | `pip install textxtract` |
| **XML** | `.xml` | Optional | `pip install textxtract[xml]` |
| **ZIP** | `.zip` | Built-in | `pip install textxtract` |

## 🔧 Advanced Usage

### Error Handling

```python
from textxtract import SyncTextExtractor
from textxtract.exceptions import (
    FileTypeNotSupportedError,
    InvalidFileError,
    ExtractionError
)

extractor = SyncTextExtractor()

try:
    text = extractor.extract("document.pdf")
    print(text)
except FileTypeNotSupportedError:
    print("❌ File type not supported")
except InvalidFileError:
    print("❌ File is invalid or corrupted")
except ExtractionError:
    print("❌ Extraction failed")
```

### Custom Configuration

```python
from textxtract import SyncTextExtractor
from textxtract import ExtractorConfig

# Custom configuration
config = ExtractorConfig(
    encoding="utf-8",
    max_file_size=50 * 1024 * 1024,  # 50MB limit
    logging_level="DEBUG"
)

extractor = SyncTextExtractor(config)
text = extractor.extract("document.pdf")
```

### Batch Processing

```python
import asyncio
from pathlib import Path
from textxtract import AsyncTextExtractor

async def process_files(file_paths):
    async with AsyncTextExtractor() as extractor:
        # Process files concurrently
        tasks = [extractor.extract(path) for path in file_paths]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        return results

# Process multiple files
files = [Path("doc1.pdf"), Path("doc2.docx"), Path("doc3.txt")]
results = asyncio.run(process_files(files))

for file, result in zip(files, results):
    if isinstance(result, Exception):
        print(f"❌ {file}: {result}")
    else:
        print(f"✅ {file}: {len(result)} characters extracted")
```

### Logging Configuration

```python
import logging
from textxtract import SyncTextExtractor

# Enable debug logging
logging.basicConfig(level=logging.DEBUG)

extractor = SyncTextExtractor()
text = extractor.extract("document.pdf")  # Will show detailed logs
```

## 🧪 Testing

```bash
# Install test dependencies
pip install textxtract[all] pytest pytest-asyncio

# Run tests
pytest

# Run with coverage
pytest --cov=textxtract
```

## 📚 Documentation

- 📖 **[Complete Documentation](https://your-org.github.io/text-extractor/)**
- 🚀 **[Installation Guide](docs/installation.md)**
- 📘 **[Usage Examples](docs/usage.md)**
- 🔍 **[API Reference](docs/api.md)**
- 🧪 **[Testing Guide](docs/testing.md)**
- 🤝 **[Contributing Guide](docs/contributing.md)**

## 🎯 Use Cases

### Document Processing
```python
from textxtract import SyncTextExtractor

def process_document(file_path):
    extractor = SyncTextExtractor()
    text = extractor.extract(file_path)
    
    # Process extracted text
    word_count = len(text.split())
    return {
        "file": file_path,
        "text": text,
        "word_count": word_count
    }
```

### Content Analysis
```python
import asyncio
from textxtract import AsyncTextExtractor

async def analyze_content(files):
    async with AsyncTextExtractor() as extractor:
        results = []
        for file in files:
            try:
                text = await extractor.extract(file)
                # Perform analysis
                analysis = {
                    "file": file,
                    "length": len(text),
                    "words": len(text.split()),
                    "contains_email": "@" in text
                }
                results.append(analysis)
            except Exception as e:
                results.append({"file": file, "error": str(e)})
        return results
```

### Data Pipeline Integration
```python
from textxtract import SyncTextExtractor

def extract_and_store(file_path, database):
    extractor = SyncTextExtractor()
    
    try:
        text = extractor.extract(file_path)
        
        # Store in database
        database.store({
            "file_path": str(file_path),
            "content": text,
            "extracted_at": datetime.now(),
            "status": "success"
        })
        
    except Exception as e:
        database.store({
            "file_path": str(file_path),
            "error": str(e),
            "extracted_at": datetime.now(),
            "status": "failed"
        })
```

## 🔧 Requirements

- **Python 3.9+**
- Optional dependencies for specific file types
- See [Installation Guide](docs/installation.md) for details

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](docs/contributing.md) for details.

### Quick Contribution Setup
```bash
# Fork and clone the repo
git clone https://github.com/10XScale-in/textxtract.git
cd text-extractor

# Set up development environment
pip install -e .[all]
pip install pytest pytest-asyncio black isort mypy

# Run tests
pytest

# Format code
black textxtract tests
isort textxtract tests
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🌟 Support

- 🐛 **Bug Reports**: [GitHub Issues](https://github.com/10XScale-in/textxtract/issues)
- 💡 **Feature Requests**: [GitHub Discussions](https://github.com/10XScale-in/textxtract/discussions)
- 📧 **Questions**: [GitHub Discussions](https://github.com/10XScale-in/textxtract/discussions)

## 🙏 Acknowledgments`

- Thanks to all contributors who have helped improve this project
- Built with Python and the amazing open-source ecosystem
- Special thanks to the maintainers of underlying libraries


