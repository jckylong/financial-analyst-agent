# app/tracing.py
"""Distributed Tracing Setup using OpenTelemetry.

Links spans across user request, subagent delegation, model reasoning,
and tool calls to Google Cloud Trace.
"""

import os
from collections.abc import Generator
from contextlib import contextmanager
from typing import Any

from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter

# Initialize global TracerProvider
provider = TracerProvider()

# If in GCP environment, try importing CloudTraceSpanExporter
try:
    from opentelemetry.exporter.gcp_trace import CloudTraceSpanExporter
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    if project_id:
        cloud_exporter = CloudTraceSpanExporter(project_id=project_id)
        provider.add_span_processor(BatchSpanProcessor(cloud_exporter))
    else:
        provider.add_span_processor(BatchSpanProcessor(ConsoleSpanExporter()))
except ImportError:
    provider.add_span_processor(BatchSpanProcessor(ConsoleSpanExporter()))

trace.set_tracer_provider(provider)
tracer = trace.get_tracer("financial_analyst_agent", "1.0.0")


@contextmanager
def trace_span(name: str, attributes: dict[str, Any] | None = None) -> Generator[trace.Span, None, None]:
    """Context manager helper to create a named OpenTelemetry trace span.

    Args:
        name: Name of the span (e.g., 'subagent.market_data', 'tool.fetch_stock_quote').
        attributes: Key-value attributes to attach to the span.

    Yields:
        Active OpenTelemetry span object.
    """
    with tracer.start_as_current_span(name) as span:
        if attributes:
            for key, val in attributes.items():
                span.set_attribute(key, str(val))
        yield span
