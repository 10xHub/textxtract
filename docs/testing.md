# Testing

Comprehensive testing guide for the `textxtract` package.

## 🧪 Running Tests

The project uses [pytest](https://pytest.org/) for all tests with support for both synchronous and asynchronous testing.

### Prerequisites

Install the package with all optional dependencies for complete testing:

```bash
pip install textxtract[all]
pip install pytest pytest-asyncio
```

### Basic Test Execution

```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run specific test file
pytest tests/test_sync.py
pytest tests/test_async.py

# Run tests with coverage
pytest --cov=textxtract
```

### Test Categories

```bash
# Run only synchronous tests
pytest tests/test_sync.py

# Run only asynchronous tests  
pytest tests/test_async.py

# Run exception handling tests
pytest tests/test_exceptions.py

# Run edge case tests
pytest tests/test_edge_cases.py
```

## 📂 Test Structure

```
tests/
├── __init__.py
├── test_sync.py          # Synchronous extractor tests
├── test_async.py         # Asynchronous extractor tests
├── test_exceptions.py    # Error handling tests
├── test_edge_cases.py    # Edge cases and validation
└── files/               # Sample test files
    ├── text_file.txt
    ├── text_file.pdf
    ├── text_file.docx
    ├── markdown.md
    ├── text.csv
    ├── text.json
    ├── text.html
    ├── text.xml
    └── ...
```

## 🔧 Test Coverage

### File Type Coverage

The test suite covers all supported file types:

| File Type | Test Files | Sync Tests | Async Tests |
|-----------|------------|------------|-------------|
| Plain Text | `text_file.txt`, `text_file.text` | ✅ | ✅ |
| Markdown | `markdown.md` | ✅ | ✅ |
| PDF | `text_file.pdf` | ✅ | ✅ |
| Word | `text_file.docx` | ✅ | ✅ |
| Legacy Word | `text_file.doc` | ✅ | ✅ |
| Rich Text | `text_file.rtf` | ✅ | ✅ |
| HTML | `text.html` | ✅ | ✅ |
| CSV | `text.csv` | ✅ | ✅ |
| JSON | `text.json` | ✅ | ✅ |
| XML | `text.xml` | ✅ | ✅ |
| ZIP | `text_zip.zip` | ✅ | ✅ |

### Input Method Coverage

- ✅ File path extraction (`extractor.extract("/path/to/file.pdf")`)
- ✅ Bytes extraction (`extractor.extract(file_bytes, "file.pdf")`)
- ✅ Both sync and async methods
- ✅ Error handling for unsupported types
- ✅ Context manager usage

### Error Handling Coverage

- ✅ `FileTypeNotSupportedError` for unsupported extensions
- ✅ `InvalidFileError` for corrupted/missing files
- ✅ `ExtractionError` for extraction failures
- ✅ `ValueError` for missing filename with bytes input

## 🎯 Writing Custom Tests

### Testing File Extraction

```python
import pytest
from pathlib import Path
from textxtract import SyncTextExtractor
from textxtract.core.exceptions import FileTypeNotSupportedError

def test_custom_file_extraction():
    extractor = SyncTextExtractor()
    
    # Test with file path
    text = extractor.extract("path/to/test/file.txt")
    assert isinstance(text, str)
    assert len(text) > 0
    
    # Test with bytes
    with open("path/to/test/file.txt", "rb") as f:
        file_bytes = f.read()
    text = extractor.extract(file_bytes, "file.txt")
    assert isinstance(text, str)
    assert len(text) > 0
```

### Testing Async Extraction

```python
import pytest
from textxtract import AsyncTextExtractor

@pytest.mark.asyncio
async def test_async_extraction():
    extractor = AsyncTextExtractor()
    
    text = await extractor.extract("path/to/test/file.txt")
    assert isinstance(text, str)
    assert len(text) > 0
```

### Testing Error Conditions

```python
import pytest
from textxtract import SyncTextExtractor
from textxtract.core.exceptions import (
    FileTypeNotSupportedError,
    InvalidFileError
)

def test_error_handling():
    extractor = SyncTextExtractor()
    
    # Test unsupported file type
    with pytest.raises(FileTypeNotSupportedError):
        extractor.extract(b"dummy", "file.unsupported")
    
    # Test missing file
    with pytest.raises(InvalidFileError):
        extractor.extract("nonexistent_file.txt")
    
    # Test missing filename with bytes
    with pytest.raises(ValueError):
        extractor.extract(b"dummy bytes")
```

## 🚀 Performance Testing

### Memory Usage Testing

```python
import psutil
import os
from textxtract import SyncTextExtractor

def test_memory_usage():
    process = psutil.Process(os.getpid())
    initial_memory = process.memory_info().rss
    
    extractor = SyncTextExtractor()
    
    # Process large file
    text = extractor.extract("large_file.pdf")
    
    final_memory = process.memory_info().rss
    memory_increase = final_memory - initial_memory
    
    # Assert reasonable memory usage
    assert memory_increase < 100 * 1024 * 1024  # Less than 100MB
```

### Concurrent Processing Testing

```python
import asyncio
import pytest
from textxtract import AsyncTextExtractor

@pytest.mark.asyncio
async def test_concurrent_extraction():
    extractor = AsyncTextExtractor()
    
    files = ["file1.txt", "file2.pdf", "file3.docx"]
    
    # Process files concurrently
    tasks = [extractor.extract(file) for file in files]
    results = await asyncio.gather(*tasks, return_exceptions=True)
    
    # Verify all succeeded
    for result in results:
        assert isinstance(result, str)
        assert len(result) > 0
```

## 🔍 Test Configuration

### pytest.ini Configuration

```ini
[tool:pytest]
minversion = 6.0
addopts = -ra -q --tb=short
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
asyncio_mode = auto
markers =
    slow: marks tests as slow (deselect with '-m "not slow"')
    integration: marks tests as integration tests
```

### Running Specific Test Categories

```bash
# Run only fast tests
pytest -m "not slow"

# Run only integration tests
pytest -m integration

# Run tests with specific keyword
pytest -k "test_sync"

# Run tests and stop on first failure
pytest -x
```

## 🐛 Debugging Tests

### Verbose Output

```bash
# Maximum verbosity
pytest -vvv

# Show local variables in tracebacks
pytest --tb=long

# Show stdout/stderr
pytest -s
```

### Debugging with pdb

```python
import pytest

def test_with_debugger():
    extractor = SyncTextExtractor()
    
    # Set breakpoint
    pytest.set_trace()
    
    text = extractor.extract("test_file.txt")
    assert text
```

## 📊 Test Reports

### Coverage Reports

```bash
# Generate coverage report
pytest --cov=textxtract --cov-report=html

# View coverage in terminal
pytest --cov=textxtract --cov-report=term-missing

# Generate XML coverage for CI
pytest --cov=textxtract --cov-report=xml
```

### JUnit XML Reports

```bash
# Generate JUnit XML for CI systems
pytest --junitxml=test-results.xml
```

## 🔄 Continuous Integration

### GitHub Actions Example

```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: [3.9, 3.10, 3.11, 3.12]
    
    steps:
    - uses: actions/checkout@v2
    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v2
      with:
        python-version: ${{ matrix.python-version }}
    
    - name: Install dependencies
      run: |
        pip install -e .[all]
        pip install pytest pytest-asyncio pytest-cov
    
    - name: Run tests
      run: pytest --cov=textxtract
```

## ✅ Validation Checklist

Before submitting changes, ensure:

- [ ] All existing tests pass
- [ ] New features have corresponding tests
- [ ] Error conditions are tested
- [ ] Both sync and async methods are tested
- [ ] Documentation examples are tested
- [ ] Performance regressions are checked
- [ ] Memory leaks are verified

## 🆘 Troubleshooting Tests

### Common Issues

**Missing dependencies:**
```bash
pip install textxtract[all] pytest pytest-asyncio
```

**Import errors:**
```python
# Ensure correct import
from textxtract import SyncTextExtractor  # Correct
from text_extractor import SyncTextExtractor  # Wrong
```

**Async test issues:**
```python
# Ensure pytest-asyncio is installed and configured
pytest.mark.asyncio  # Required for async tests
```

**File not found errors:**
```python
# Use absolute paths in tests
TEST_FILES_DIR = Path(__file__).parent / "files"
file_path = TEST_FILES_DIR / "test_file.txt"
```

For more testing help, see the [API Reference](api.md) or [Usage Guide](usage.md).