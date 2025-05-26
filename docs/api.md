# API Reference

Complete API reference for the `textxtract` package.

## Core Classes

### SyncTextExtractor

The synchronous text extractor for blocking operations.

```python
from textxtract import SyncTextExtractor
```

#### Constructor

```python
SyncTextExtractor(config: Optional[ExtractorConfig] = None)
```

**Parameters:**
- `config` (optional): Configuration object for customizing extraction behavior

#### Methods

##### extract()

```python
extract(
    source: Union[Path, str, bytes], 
    filename: Optional[str] = None, 
    config: Optional[dict] = None
) -> str
```

Extract text synchronously from file path or bytes.

**Parameters:**
- `source`: File path (Path/str) or file bytes
- `filename`: Required if source is bytes, optional for file paths
- `config`: Optional configuration overrides

**Returns:**
- `str`: Extracted text

**Raises:**
- `ValueError`: If filename is missing when source is bytes
- `FileTypeNotSupportedError`: If file extension is not supported
- `InvalidFileError`: If file is invalid or corrupted
- `ExtractionError`: If extraction fails

**Examples:**

```python
extractor = SyncTextExtractor()

# From file path
text = extractor.extract("document.pdf")
text = extractor.extract(Path("document.pdf"))

# From bytes (filename required)
with open("document.pdf", "rb") as f:
    file_bytes = f.read()
text = extractor.extract(file_bytes, "document.pdf")

# With custom config
config = {"encoding": "utf-8", "max_file_size": 50*1024*1024}
text = extractor.extract("document.pdf", config=config)
```

#### Context Manager Support

```python
with SyncTextExtractor() as extractor:
    text = extractor.extract("document.pdf")
```

---

### AsyncTextExtractor

The asynchronous text extractor for non-blocking operations.

```python
from textxtract import AsyncTextExtractor
```

#### Constructor

```python
AsyncTextExtractor(config: Optional[ExtractorConfig] = None)
```

**Parameters:**
- `config` (optional): Configuration object for customizing extraction behavior

#### Methods

##### extract()

```python
async extract(
    source: Union[Path, str, bytes], 
    filename: Optional[str] = None, 
    config: Optional[dict] = None
) -> str
```

Extract text asynchronously from file path or bytes using thread pool.

**Parameters:**
- `source`: File path (Path/str) or file bytes
- `filename`: Required if source is bytes, optional for file paths
- `config`: Optional configuration overrides

**Returns:**
- `str`: Extracted text

**Raises:**
- `ValueError`: If filename is missing when source is bytes
- `FileTypeNotSupportedError`: If file extension is not supported
- `InvalidFileError`: If file is invalid or corrupted
- `ExtractionError`: If extraction fails

**Examples:**

```python
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

#### Context Manager Support

```python
async with AsyncTextExtractor() as extractor:
    text = await extractor.extract("document.pdf")
```

---

## Configuration

### ExtractorConfig

Configuration class for customizing extraction behavior.

```python
from textxtract.core.config import ExtractorConfig
```

#### Constructor

```python
ExtractorConfig(
    encoding: str = "utf-8",
    max_file_size: int = 100 * 1024 * 1024,  # 100MB
    logging_level: str = "INFO"
)
```

**Parameters:**
- `encoding`: Default text encoding
- `max_file_size`: Maximum file size in bytes
- `logging_level`: Logging verbosity level

**Example:**

```python
config = ExtractorConfig(
    encoding="utf-8",
    max_file_size=50 * 1024 * 1024,  # 50MB
    logging_level="DEBUG"
)

extractor = SyncTextExtractor(config)
```

---

## Exceptions

All exceptions are in the `textxtract.core.exceptions` module.

### ExtractionError

Base exception for all extraction-related errors.

```python
from textxtract.core.exceptions import ExtractionError
```

### FileTypeNotSupportedError

Raised when the file extension is not supported.

```python
from textxtract.core.exceptions import FileTypeNotSupportedError
```

### InvalidFileError

Raised when the file is invalid, corrupted, or not found.

```python
from textxtract.core.exceptions import InvalidFileError
```

### ExtractionTimeoutError

Raised when extraction exceeds the allowed timeout.

```python
from textxtract.core.exceptions import ExtractionTimeoutError
```

**Example Error Handling:**

```python
from textxtract import SyncTextExtractor
from textxtract.core.exceptions import (
    ExtractionError,
    FileTypeNotSupportedError,
    InvalidFileError
)

extractor = SyncTextExtractor()

try:
    text = extractor.extract("document.pdf")
except FileTypeNotSupportedError as e:
    print(f"Unsupported file type: {e}")
except InvalidFileError as e:
    print(f"Invalid file: {e}")
except ExtractionError as e:
    print(f"Extraction failed: {e}")
```

---

## Utilities

### FileInfo

Data class containing file information.

```python
from textxtract.core.utils import FileInfo
```

#### Attributes

- `filename`: str - Name of the file
- `size_bytes`: int - File size in bytes
- `size_mb`: float - File size in megabytes
- `size_kb`: float - File size in kilobytes (property)
- `extension`: str - File extension
- `is_temp`: bool - Whether file is temporary

---

## Supported File Types

| Extension | Handler Class | Optional Dependency |
|-----------|---------------|-------------------|
| `.txt`, `.text` | `TXTHandler` | None |
| `.pdf` | `PDFHandler` | `pymupdf` |
| `.docx` | `DOCXHandler` | `python-docx` |
| `.doc` | `DOCHandler` | `antiword` |
| `.md` | `MDHandler` | `markdown`, `beautifulsoup4` |
| `.rtf` | `RTFHandler` | `pyrtf-ng` |
| `.html`, `.htm` | `HTMLHandler` | `beautifulsoup4`, `lxml` |
| `.csv` | `CSVHandler` | None |
| `.json` | `JSONHandler` | None |
| `.xml` | `XMLHandler` | `lxml` |
| `.zip` | `ZIPHandler` | None |

---

## Logging

The package uses Python's standard logging module with the following loggers:

- `textxtract.sync` - Synchronous extractor logs
- `textxtract.aio` - Asynchronous extractor logs
- `textxtract.utils` - Utility function logs

**Configure logging:**

```python
import logging

# Set debug level for detailed logs
logging.basicConfig(level=logging.DEBUG)

# Or configure specific logger
logger = logging.getLogger("textxtract")
logger.setLevel(logging.INFO)
```

---

## Type Hints

The package is fully typed. Import types for better IDE support:

```python
from typing import Union, Optional
from pathlib import Path
from textxtract import SyncTextExtractor, AsyncTextExtractor
from textxtract.core.config import ExtractorConfig
from textxtract.core.exceptions import ExtractionError