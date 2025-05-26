# Testing

## Running the Test Suite

This project uses [pytest](https://pytest.org/) for all tests.

### Run all tests

```bash
pytest
```

### Run a specific test file

```bash
pytest textxtract/tests/test_sync.py
pytest textxtract/tests/test_async.py
```

### Run tests with extra dependencies

If you want to test extraction for optional file types, install the relevant extras:

```bash
pip install text-extractor[all]
pytest
```

## Test Coverage

- Handlers for all supported file types
- Error handling and exceptions
- Synchronous and asynchronous extractors
- Edge cases and invalid files

## Adding New Tests

1. Add your test file in `textxtract/tests/` or `textxtract/tests/test_handlers/`.
2. Use descriptive test names and docstrings.
3. Run `pytest` to verify.