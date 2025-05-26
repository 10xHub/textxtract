# API Reference

## Extractors

### `SyncTextExtractor`

- **Location:** `from textxtract import SyncTextExtractor`
- **Methods:**
  - `extract(file_bytes: bytes, filename: str, config: Optional[dict] = None) -> str`
  - `extract_async(...)` (raises NotImplementedError)

### `AsyncTextExtractor`

- **Location:** `from textxtract.aio import AsyncTextExtractor`
- **Methods:**
  - `extract_async(file_bytes: bytes, filename: str, config: Optional[dict] = None) -> str`
  - `extract(...)` (raises NotImplementedError)

## Exceptions

- `ExtractionError`
- `InvalidFileError`
- `FileTypeNotSupportedError`
- `ExtractionTimeoutError`

## Handlers

Each file type has a handler class in `textxtract.handlers` (e.g., `PDFHandler`, `DOCXHandler`, etc.), all implementing:

- `extract(file_path: Path, config: Optional[dict] = None) -> str`
- `extract_async(file_path: Path, config: Optional[dict] = None) -> str`

## Configuration

- `ExtractorConfig` in `textxtract.core.config`
- Register custom handlers, set encoding, logging, and timeouts.

## Logging

- Uses Python's `logging` module.
- Configure via `logging.basicConfig(level=logging.DEBUG)`.