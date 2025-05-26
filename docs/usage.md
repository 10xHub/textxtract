# Usage

## Synchronous Extraction

```python
from textxtract import SyncTextExtractor

# file_bytes: bytes of your file
# filename: name of your file (e.g. "document.pdf")
extractor = SyncTextExtractor()
text = extractor.extract(file_bytes, filename)
print(text)
```

## Asynchronous Extraction

```python
from textxtract.aio import AsyncTextExtractor
import asyncio

extractor = AsyncTextExtractor()
text = asyncio.run(extractor.extract_async(file_bytes, filename))
print(text)
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

## Error Handling

All extractors raise custom exceptions from `textxtract.core.exceptions`:
- `ExtractionError`
- `InvalidFileError`
- `FileTypeNotSupportedError`
- `ExtractionTimeoutError`

## Logging

Configure logging as desired. By default, debug and info logs are available:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Custom Handlers

You can register your own file type handlers via the configuration API.