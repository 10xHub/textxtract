# Contributing

Thank you for your interest in contributing to **textxtract**! We welcome contributions of all kinds, from bug reports to new features.

## 🚀 Quick Start for Contributors

### 1. Development Setup

```bash
# Fork and clone the repository
git clone https://github.com/10XScale-in/textxtract.git
cd textxtract

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode with all dependencies
pip install -e .[all]

# Install development tools
pip install pytest pytest-asyncio pytest-cov black isort mypy pre-commit
```

### 2. Development Workflow

```bash
# Create a feature branch
git checkout -b feature/your-feature-name

# Make your changes
# ... edit code ...

# Run tests
pytest

# Format code
black textxtract tests
isort textxtract tests

# Type check
mypy textxtract

# Commit your changes
git add .
git commit -m "feat: add your feature description"

# Push and create PR
git push origin feature/your-feature-name
```

## 📋 Contribution Guidelines

### Code Style

We follow these conventions:

- **PEP 8** for Python code style
- **Black** for code formatting
- **isort** for import sorting
- **Type hints** for all public APIs
- **Docstrings** for all public functions and classes

### Code Formatting

```bash
# Format code with black
black textxtract tests

# Sort imports
isort textxtract tests

# Check formatting
black --check textxtract tests
isort --check textxtract tests
```

### Type Checking

```bash
# Run type checking
mypy textxtract

# Check specific file
mypy textxtract/sync/extractor.py
```

## 🧪 Testing Requirements

### Writing Tests

All contributions must include appropriate tests:

```python
# Example test structure
import pytest
from pathlib import Path
from textxtract import SyncTextExtractor
from textxtract.exceptions import FileTypeNotSupportedError

def test_new_feature():
    """Test description of the new feature."""
    extractor = SyncTextExtractor()
    
    # Test successful case
    result = extractor.extract("test_file.txt")
    assert isinstance(result, str)
    assert len(result) > 0
    
    # Test error case
    with pytest.raises(FileTypeNotSupportedError):
        extractor.extract(b"dummy", "file.unsupported")

@pytest.mark.asyncio
async def test_async_feature():
    """Test async functionality."""
    from textxtract import AsyncTextExtractor
    
    extractor = AsyncTextExtractor()
    result = await extractor.extract("test_file.txt")
    assert isinstance(result, str)
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=textxtract --cov-report=html

# Run specific test categories
pytest tests/test_sync.py
pytest tests/test_async.py

# Run performance tests
pytest -m slow
```

### Test Coverage Requirements

- All new code must have **90%+ test coverage**
- Both sync and async paths must be tested
- Error conditions must be tested
- Integration tests for new file types

## 🏗️ Adding New File Type Support

### 1. Create Handler Class

```python
# textxtract/handlers/your_format.py
"""Handler for YOUR_FORMAT files."""

from pathlib import Path
from typing import Optional
from textxtract.core.base import FileTypeHandler
from textxtract.exceptions import ExtractionError

class YourFormatHandler(FileTypeHandler):
    """Handler for extracting text from YOUR_FORMAT files."""

    def extract(self, file_path: Path, config: Optional[dict] = None) -> str:
        try:
            # Check for required dependency
            try:
                import your_library
            except ImportError:
                raise ExtractionError(
                    "your_library is not installed. "
                    "Install with 'pip install textxtract[your_format]'"
                )
            
            # Extract text logic
            with open(file_path, 'rb') as f:
                content = your_library.extract_text(f)
            
            return content
            
        except Exception as e:
            raise ExtractionError(f"YOUR_FORMAT extraction failed: {e}")

    async def extract_async(self, file_path: Path, config: Optional[dict] = None) -> str:
        import asyncio
        return await asyncio.to_thread(self.extract, file_path, config)
```

### 2. Register Handler

Add to the registry in `textxtract/core/registry.py`:

```python
from textxtract.handlers.your_format import YourFormatHandler

# Add to handler map
HANDLER_MAP = {
    # ... existing handlers ...
    ".your_ext": YourFormatHandler,
}
```

### 3. Update Dependencies

Add to `pyproject.toml`:

```toml
[project.optional-dependencies]
your_format = ["your_library>=1.0.0"]
all = [
    # ... existing dependencies ...
    "your_library>=1.0.0",
]
```

### 4. Add Tests

Create test files and test cases:

```python
# tests/test_your_format.py
import pytest
from pathlib import Path
from textxtract import SyncTextExtractor, AsyncTextExtractor

TEST_FILES_DIR = Path(__file__).parent / "files"

def test_your_format_sync():
    extractor = SyncTextExtractor()
    text = extractor.extract(TEST_FILES_DIR / "test_file.your_ext")
    assert isinstance(text, str)
    assert len(text) > 0

@pytest.mark.asyncio
async def test_your_format_async():
    extractor = AsyncTextExtractor()
    text = await extractor.extract(TEST_FILES_DIR / "test_file.your_ext")
    assert isinstance(text, str)
    assert len(text) > 0
```

### 5. Update Documentation

Update the following files:
- `docs/usage.md` - Add your format to supported types table
- `docs/installation.md` - Add installation instructions
- `docs/api.md` - Document the new handler

## 🐛 Bug Reports

### Before Reporting

1. Check existing issues
2. Verify with latest version
3. Create minimal reproduction case

### Bug Report Template

```markdown
**Bug Description**
Clear description of the bug.

**Steps to Reproduce**
1. Step one
2. Step two
3. ...

**Expected Behavior**
What should happen.

**Actual Behavior**
What actually happens.

**Environment**
- OS: [e.g., Ubuntu 20.04]
- Python: [e.g., 3.9.7]
- textxtract: [e.g., 0.2.0]
- Dependencies: [relevant package versions]

**Code Sample**
```python
from textxtract import SyncTextExtractor

extractor = SyncTextExtractor()
# Code that reproduces the issue
```

**Error Messages**
```
Full error traceback
```
```

## 💡 Feature Requests

### Feature Request Template

```markdown
**Feature Description**
Clear description of the proposed feature.

**Use Case**
Why is this feature needed? What problem does it solve?

**Proposed API**
```python
# Example of how the feature would be used
```

**Alternatives Considered**
Other approaches you've considered.

**Additional Context**
Any other relevant information.
```

## 📝 Documentation Contributions

### Documentation Structure

```
docs/
├── index.md           # Main landing page
├── installation.md    # Installation guide
├── usage.md          # Usage examples
├── api.md            # API reference
├── testing.md        # Testing guide
├── contributing.md   # This file
└── changelog.md      # Version history
```

### Writing Guidelines

- Use clear, concise language
- Include working code examples
- Test all code examples
- Use consistent formatting
- Add cross-references between sections

### Building Documentation

```bash
# Install MkDocs
pip install mkdocs mkdocs-material

# Serve documentation locally
mkdocs serve

# Build documentation
mkdocs build
```

## 🔄 Release Process

### Versioning

We follow [Semantic Versioning](https://semver.org/):

- **MAJOR**: Breaking changes
- **MINOR**: New features (backward compatible)
- **PATCH**: Bug fixes (backward compatible)

### Release Checklist

- [ ] Update version in `pyproject.toml`
- [ ] Update `CHANGELOG.md`
- [ ] Run full test suite
- [ ] Update documentation
- [ ] Create release PR
- [ ] Tag release after merge
- [ ] Publish to PyPI

## 🤝 Code of Conduct

### Our Standards

- Be respectful and inclusive
- Provide constructive feedback
- Focus on what's best for the community
- Show empathy towards other contributors

### Unacceptable Behavior

- Harassment or discrimination
- Trolling or insulting comments
- Publishing private information
- Unprofessional conduct

Thank you for helping make textxtract better! 🎉