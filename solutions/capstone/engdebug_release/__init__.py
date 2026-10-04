"""engdebug_release: a sensor-data pipeline for learning to test, debug and optimise Python code.

This package is the *reference* (working) implementation. The labs in ``labs/`` ship deliberately broken
copies of these modules; the job is to find and fix the bugs and make the tests pass.

Modules
-------
exceptions    the pipeline's exception hierarchy
ingestion     reading sensor CSV files into records
validation    schema, type and range checks on records
calculations  engineering calculations: efficiency, drift, moving averages, anomaly scores, unit conversions
models        Sensor and Equipment classes with invariants
alerting      threshold and trend alerts
reporting     daily summary reports (text and JSON)
pipeline      the end-to-end run: ingest -> validate -> calculate -> alert -> report
logsetup      structured logging configuration
"""

from . import alerting, calculations, exceptions, ingestion, logsetup, models, pipeline, reporting, validation

__version__ = "0.2.0"
__all__ = ["__version__", "alerting", "calculations", "exceptions", "ingestion", "logsetup", "models", "pipeline", "reporting", "validation"]
