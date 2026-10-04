"""The pipeline's exception hierarchy.

Every error the pipeline raises on purpose derives from ``PipelineError``, so callers can catch the whole
family with one clause and still distinguish the kinds. Each exception carries context (which file, which
row, which field) because a message like "invalid value" is useless at 3 a.m.
"""

from __future__ import annotations


class PipelineError(Exception):
    """Base class for every error raised deliberately by the pipeline."""


class IngestionError(PipelineError):
    """A file could not be read or parsed into records."""

    def __init__(self, path, message: str, row: int | None = None):
        self.path = str(path)
        self.row = row
        where = f"{self.path}" + (f", row {row}" if row is not None else "")
        super().__init__(f"{where}: {message}")


class ValidationError(PipelineError):
    """A record violated the schema or a range check."""

    def __init__(self, message: str, field: str | None = None, row: int | None = None, value=None):
        self.field = field
        self.row = row
        self.value = value
        parts = [message]
        if field is not None:
            parts.append(f"field={field!r}")
        if row is not None:
            parts.append(f"row={row}")
        if value is not None:
            parts.append(f"value={value!r}")
        super().__init__("; ".join(parts))


class CalculationError(PipelineError):
    """An engineering calculation received inputs it cannot handle (e.g. zero input power)."""


class ConfigError(PipelineError):
    """The pipeline configuration is missing a key or holds an invalid value."""
