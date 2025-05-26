# Text Extractor

A robust, extensible Python package for synchronous and asynchronous text extraction from PDF, DOCX, DOC, TXT, and ZIP files.

## Features

- Synchronous and asynchronous extraction APIs
- Modular file type handlers (PDF, DOCX, DOC, TXT, ZIP)
- Abstract base classes for extensibility
- Custom exception handling and logging
- Configurable encoding, logging, and timeouts
- Easy to add new file type handlers
- Comprehensive unit tests with pytest

## Installation

```bash
pip install .
```

## Usage Example

```python
from text_extractor.sync.extractor import SyncTextExtractor
from text_extractor.async_.extractor import AsyncTextExtractor

# Synchronous extraction
extractor = SyncTextExtractor()
text = extractor.extract(file_bytes, filename)

# Asynchronous extraction
import asyncio
async_extractor = AsyncTextExtractor()
text = asyncio.run(async_extractor.extract_async(file_bytes, filename))
```

## API Reference

See [`ARCHITECTURE_PLAN.md`](ARCHITECTURE_PLAN.md) for detailed architecture and module layout.

## Running Tests

```bash
pytest
```

## Contributing

1. Fork the repository.
2. Create a new branch.
3. Add your feature or fix.
4. Write tests.
5. Submit a pull request.

## License

MIT License

