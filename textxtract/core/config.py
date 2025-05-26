"""Configuration and customization for textxtract package."""

import os
from typing import Callable, Dict, Optional, Any, Union
from pathlib import Path


class ExtractorConfig:
    """Enhanced configuration options for text extraction with validation."""

    def __init__(
        self,
        encoding: str = "utf-8",
        logging_level: str = "INFO",
        logging_format: Optional[str] = None,
        timeout: Optional[float] = None,
        max_file_size: Optional[int] = None,
        max_memory_usage: Optional[int] = None,
        custom_handlers: Optional[Dict[str, Callable]] = None,
        **kwargs,
    ):
        # Validate and set basic options
        self.encoding = self._validate_encoding(encoding)
        self.logging_level = self._validate_logging_level(logging_level)
        self.logging_format = (
            logging_format or "%(asctime)s %(levelname)s %(name)s: %(message)s"
        )
        self.timeout = self._validate_timeout(timeout)
        self.max_file_size = self._validate_max_file_size(max_file_size)
        self.max_memory_usage = max_memory_usage
        self.custom_handlers = custom_handlers or {}

        # Load from environment variables
        self._load_from_env()

        # Store additional kwargs for handler-specific config
        self.extra_config = kwargs

    def _validate_encoding(self, encoding: str) -> str:
        """Validate encoding parameter."""
        if not isinstance(encoding, str):
            raise ValueError("Encoding must be a string")

        # Test if encoding is valid
        try:
            "test".encode(encoding)
        except LookupError:
            raise ValueError(f"Invalid encoding: {encoding}")

        return encoding

    def _validate_logging_level(self, level: str) -> str:
        """Validate logging level parameter."""
        valid_levels = {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}
        if level.upper() not in valid_levels:
            raise ValueError(
                f"Invalid logging level: {level}. Must be one of {valid_levels}"
            )
        return level.upper()

    def _validate_timeout(self, timeout: Optional[float]) -> Optional[float]:
        """Validate timeout parameter."""
        if timeout is not None:
            if not isinstance(timeout, (int, float)) or timeout <= 0:
                raise ValueError("Timeout must be a positive number")
        return timeout

    def _validate_max_file_size(self, size: Optional[int]) -> Optional[int]:
        """Validate max file size parameter."""
        if size is not None:
            if not isinstance(size, int) or size <= 0:
                raise ValueError("Max file size must be a positive integer")
        return size

    def _load_from_env(self):
        """Load configuration from environment variables."""
        # Override with environment variables if present
        env_encoding = os.getenv("TEXT_EXTRACTOR_ENCODING")
        if env_encoding:
            self.encoding = self._validate_encoding(env_encoding)

        env_logging = os.getenv("TEXT_EXTRACTOR_LOG_LEVEL")
        if env_logging:
            self.logging_level = self._validate_logging_level(env_logging)

        env_timeout = os.getenv("TEXT_EXTRACTOR_TIMEOUT")
        if env_timeout:
            try:
                self.timeout = float(env_timeout)
            except ValueError:
                pass  # Ignore invalid values

        env_max_size = os.getenv("TEXT_EXTRACTOR_MAX_FILE_SIZE")
        if env_max_size:
            try:
                self.max_file_size = int(env_max_size)
            except ValueError:
                pass  # Ignore invalid values

    def register_handler(self, extension: str, handler: Callable):
        """Register a custom file type handler."""
        if not extension.startswith("."):
            extension = f".{extension}"
        self.custom_handlers[extension.lower()] = handler

    def get_handler(self, extension: str) -> Optional[Callable]:
        """Retrieve a handler for a given file extension."""
        return self.custom_handlers.get(extension.lower())

    def get_handler_config(self, handler_name: str) -> Dict[str, Any]:
        """Get configuration specific to a handler."""
        base_config = {
            "encoding": self.encoding,
            "timeout": self.timeout,
            "max_file_size": self.max_file_size,
            "max_memory_usage": self.max_memory_usage,
        }

        # Add handler-specific config
        handler_config_key = f"{handler_name.lower()}_config"
        if handler_config_key in self.extra_config:
            base_config.update(self.extra_config[handler_config_key])

        return base_config

    def to_dict(self) -> Dict[str, Any]:
        """Convert configuration to dictionary."""
        return {
            "encoding": self.encoding,
            "logging_level": self.logging_level,
            "logging_format": self.logging_format,
            "timeout": self.timeout,
            "max_file_size": self.max_file_size,
            "max_memory_usage": self.max_memory_usage,
            "custom_handlers": {k: str(v) for k, v in self.custom_handlers.items()},
            **self.extra_config,
        }

    @classmethod
    def from_file(cls, config_path: Union[str, Path]) -> "ExtractorConfig":
        """Load configuration from a file (JSON, YAML, or TOML)."""
        config_path = Path(config_path)

        if not config_path.exists():
            raise FileNotFoundError(f"Configuration file not found: {config_path}")

        content = config_path.read_text()

        if config_path.suffix.lower() == ".json":
            import json

            config_data = json.loads(content)
        elif config_path.suffix.lower() in (".yaml", ".yml"):
            try:
                import yaml

                config_data = yaml.safe_load(content)
            except ImportError:
                raise ImportError("PyYAML is required to load YAML configuration files")
        elif config_path.suffix.lower() == ".toml":
            try:
                import tomli

                config_data = tomli.loads(content)
            except ImportError:
                raise ImportError("tomli is required to load TOML configuration files")
        else:
            raise ValueError(
                f"Unsupported configuration file format: {config_path.suffix}"
            )

        return cls(**config_data)

    def __repr__(self) -> str:
        return f"ExtractorConfig(encoding='{self.encoding}', logging_level='{self.logging_level}', timeout={self.timeout})"
