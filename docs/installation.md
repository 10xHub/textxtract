# Installation

Text Extractor is designed to be lightweight and modular, allowing you to install only the dependencies you need for your specific use case.

## 📦 Basic Installation

Install the core package without optional dependencies:

```bash
pip install textxtract
```

This provides basic text extraction for:
- `.txt` and `.text` files
- `.csv` files  
- `.json` files
- `.zip` archives

## 🎯 Install with File Type Support

Install support for specific file types using optional extras:

### Individual File Types

```bash
# PDF support
pip install textxtract[pdf]

# Microsoft Word (.docx) support
pip install textxtract[docx]

# Legacy Word (.doc) support
pip install textxtract[doc]

# Markdown support
pip install textxtract[md]

# Rich Text Format support
pip install textxtract[rtf]

# HTML support
pip install textxtract[html]

# XML support
pip install textxtract[xml]
```

### Multiple File Types

```bash
# Install support for multiple formats
pip install textxtract[pdf,docx,html]

# Install all supported formats
pip install textxtract[all]
```

## 🔧 Available Extras

| Extra | Dependencies | File Types Supported |
|-------|-------------|---------------------|
| `pdf` | `pymupdf` | `.pdf` |
| `docx` | `python-docx` | `.docx` |
| `doc` | `antiword` | `.doc` |
| `md` | `markdown`, `beautifulsoup4` | `.md` |
| `rtf` | `striprtf` | `.rtf` |
| `html` | `beautifulsoup4`, `lxml` | `.html`, `.htm` |
| `xml` | `lxml` | `.xml` |
| `all` | All of the above | All supported types |

## 🐍 Python Version Requirements

- **Python 3.9 or higher** is required
- Tested on Python 3.9, 3.10, 3.11, 3.12, and 3.13

## 🔄 Upgrading

To upgrade to the latest version:

```bash
pip install --upgrade textxtract
```

To upgrade with all extras:

```bash
pip install --upgrade textxtract[all]
```

## 🚀 Development Installation

For development or contributing:

```bash
# Clone the repository
git clone https://github.com/your-org/text-extractor.git
cd text-extractor

# Install in development mode with all dependencies
pip install -e .[all]

# Install development dependencies
pip install pytest pytest-asyncio
```

## 📋 System Requirements

### For `.doc` files (antiword)
On Ubuntu/Debian:
```bash
sudo apt-get install antiword
```

On macOS:
```bash
brew install antiword
```

On Windows:
Download antiword from the official website and ensure it's in your PATH.

## ✅ Verify Installation

Test your installation:

```python
from textxtract import SyncTextExtractor

extractor = SyncTextExtractor()
print("Installation successful!")
```

## 🐛 Troubleshooting

### Common Issues

**Import Error**: Make sure you have the correct package name:
```python
# Correct
from textxtract import SyncTextExtractor

# Incorrect
from text_extractor import SyncTextExtractor
```

**Missing Dependencies**: Install the required extras for your file types:
```bash
pip install textxtract[pdf]  # For PDF support
```

**Permission Errors**: On some systems, you may need to install with user permissions:
```bash
pip install --user textxtract
```

## 🆘 Getting Help

If you encounter issues:

1. Check the [Usage Guide](usage.md) for examples
2. Review the [API Documentation](api.md)
3. Look at the [Testing Guide](testing.md) for validation
4. Open an issue on our GitHub repository