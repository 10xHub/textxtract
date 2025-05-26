# Installation

## Basic Install

Install the core package (no extra dependencies):

```bash
pip install text-extractor

```

## Optional File Type Support

Install with support for specific file types:

```bash
pip install text-extractor[pdf]
pip install text-extractor[docx]
pip install text-extractor[md]
pip install text-extractor[rtf]
pip install text-extractor[html]
pip install text-extractor[all]  # All supported types
```

See [pyproject.toml](../pyproject.toml) for all available extras.

## Requirements

- Python 3.9+
- Optional: Only the dependencies for the file types you use

## Upgrading

```bash
pip install --upgrade text-extractor
```