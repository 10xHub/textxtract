"""Logging configuration for textxtract package."""

import logging


def setup_logging(
    level: str = "INFO", fmt: str = "%(asctime)s %(levelname)s %(name)s: %(message)s"
):
    """Configure logging for the package."""
    logging.basicConfig(level=getattr(logging, level.upper(), logging.INFO), format=fmt)
