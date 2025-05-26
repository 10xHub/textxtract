# Usage

The text extractor provides both synchronous and asynchronous extractors that support both file paths and bytes input for maximum flexibility.

## Basic Usage

```python
from textxtract import SyncTextExtractor, AsyncTextExtractor

# Synchronous extractor
sync_extractor = SyncTextExtractor()

# Asynchronous extractor
async_extractor = AsyncTextExtractor()
```

## Extracting from File Paths

### Synchronous

```python
from textxtract import SyncTextExtractor

extractor = SyncTextExtractor()

# From file path (string)
text = extractor.extract("document.pdf")

# From Path object
from pathlib import Path
text = extractor.extract(Path("document.pdf"))
```

### Asynchronous

```python
from textxtract import AsyncTextExtractor
import asyncio

extractor = AsyncTextExtractor()

# Async extraction from file path
text = await extractor.extract_async("document.pdf")

# Or using asyncio.run for simple cases
text = asyncio.run(extractor.extract_async("document.pdf"))
```

## Extracting from Bytes

When working with bytes, the filename parameter is **required** for file type detection:

### Synchronous

```python
from textxtract import SyncTextExtractor

extractor = SyncTextExtractor()

# From bytes (filename required for extension detection)
with open("document.pdf", "rb") as f:
    file_bytes = f.read()

text = extractor.extract(file_bytes, "document.pdf")
```

### Asynchronous

```python
from textxtract import AsyncTextExtractor

extractor = AsyncTextExtractor()

# Async extraction from bytes
with open("document.pdf", "rb") as f:
    file_bytes = f.read()

text = await extractor.extract_async(file_bytes, "document.pdf")
```

## Supported File Types

| Extension | Extra Dependency      | Handler         |
|-----------|----------------------|-----------------|
| .pdf      | [pdf]                | PyMuPDF         |
| .docx     | [docx]               | python-docx     |
| .doc      | [doc]                | antiword        |
| .txt      |                      | stdlib          |
| .md       | [md]                 | markdown        |
| .rtf      | [rtf]                | pyrtf-ng        |
| .html/.htm| [html]               | beautifulsoup4  |
| .csv      |                      | stdlib          |
| .json     |                      | stdlib          |
| .xml      | [xml]                | lxml            |
| .zip      |                      | stdlib          |

## Configuration

```python
from textxtract import SyncTextExtractor
from textxtract.core.config import ExtractorConfig

# Custom configuration
config = ExtractorConfig(
    encoding="utf-8",
    logging_level="DEBUG"
)

extractor = SyncTextExtractor(config)
```

## Error Handling

All operations raise custom exceptions from `textxtract.core.exceptions`:

```python
from textxtract import SyncTextExtractor
from textxtract.core.exceptions import (
    ExtractionError,
    InvalidFileError,
    FileTypeNotSupportedError
)

extractor = SyncTextExtractor()

try:
    text = extractor.extract("document.pdf")
except FileTypeNotSupportedError:
    print("File type not supported")
except InvalidFileError:
    print("File is invalid or corrupted")
except ExtractionError:
    print("General extraction error")
```

## Context Manager Support

Both extractors support context managers for proper resource cleanup:

### Synchronous

```python
from textxtract import SyncTextExtractor

with SyncTextExtractor() as extractor:
    text = extractor.extract("document.pdf")
```

### Asynchronous

```python
from textxtract import AsyncTextExtractor

async with AsyncTextExtractor() as extractor:
    text = await extractor.extract_async("document.pdf")
```

## Logging

Configure logging to see extraction progress:

```python
import logging
logging.basicConfig(level=logging.DEBUG)

# Now extraction will log debug information
from textxtract import SyncTextExtractor
extractor = SyncTextExtractor()
text = extractor.extract("document.pdf")
```

## Batch Processing

### Synchronous Batch Processing

```python
from textxtract import SyncTextExtractor
from pathlib import Path

def process_files_sync(file_paths):
    extractor = SyncTextExtractor()
    results = []
    for path in file_paths:
        try:
            text = extractor.extract(path)
            results.append({"file": path, "text": text, "success": True})
        except Exception as e:
            results.append({"file": path, "error": str(e), "success": False})
    return results

file_paths = [Path("doc1.pdf"), Path("doc2.docx"), Path("doc3.txt")]
results = process_files_sync(file_paths)
```

### Asynchronous Batch Processing

```python
import asyncio
from textxtract import AsyncTextExtractor
from pathlib import Path

async def process_files_async(file_paths):
    async with AsyncTextExtractor() as extractor:
        tasks = [extractor.extract_async(path) for path in file_paths]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        return results

# Process multiple files concurrently
file_paths = [Path("doc1.pdf"), Path("doc2.docx"), Path("doc3.txt")]
results = asyncio.run(process_files_async(file_paths))
```

## Advanced Usage

### Custom Configuration per Extraction

```python
from textxtract import SyncTextExtractor

extractor = SyncTextExtractor()

# Override config for specific extraction
custom_config = {
    "encoding": "latin-1",
    "max_file_size": 50 * 1024 * 1024  # 50MB
}

text = extractor.extract("document.pdf", config=custom_config)
```

### Working with Large Files

```python
from textxtract import AsyncTextExtractor
import asyncio

async def extract_large_file():
    async with AsyncTextExtractor() as extractor:
        # For large files, async extraction is recommended
        config = {"max_file_size": 500 * 1024 * 1024}  # 500MB
        text = await extractor.extract_async("large_document.pdf", config=config)
        return text

text = asyncio.run(extract_large_file())
```

## Important Notes

1. **File Extensions Required**: Files must have extensions for type detection
2. **Filename Required for Bytes**: When passing bytes, filename parameter is mandatory
3. **Async vs Sync**: Use AsyncTextExtractor for I/O-bound operations and concurrent processing
4. **Resource Cleanup**: Use context managers for automatic resource cleanup
5. **Error Handling**: Always handle exceptions appropriately for production use