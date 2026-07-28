# app/logger.py
"""Structured JSON Logging System.

Configures structlog to output structured JSON logs containing timestamp,
conversation_id, trace_id, agent_name, tool_name, and event stage (INTENT vs OUTCOME).
Includes automatic PII redaction via app.sanitizer.
"""

import logging
import sys
from typing import Any

import structlog

from app.sanitizer import structlog_pii_sanitizer_processor


def configure_logging(level: str = "INFO") -> None:
    """Configures global structlog and standard python logging handlers.

    Args:
        level: Logging level string ('DEBUG', 'INFO', 'WARNING', 'ERROR').
    """
    log_level = getattr(logging, level.upper(), logging.INFO)

    logging.basicConfig(
        format="%(message)s",
        stream=sys.stdout,
        level=log_level,
    )

    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,
            structlog.processors.add_log_level,
            structlog.processors.TimeStamper(fmt="iso"),
            structlog_pii_sanitizer_processor,  # Active PII / Secret Redaction
            structlog.processors.JSONRenderer(),
        ],
        wrapper_class=structlog.make_filtering_bound_logger(log_level),
        context_class=dict,
        logger_factory=structlog.PrintLoggerFactory(),
        cache_logger_on_first_use=True,
    )


logger = structlog.get_logger("financial_analyst_agent")


def log_tool_intent(agent_name: str, tool_name: str, args: dict[str, Any], conversation_id: str | None = None) -> None:
    """Log the intended action before executing a tool (INTENT).

    Args:
        agent_name: Name of the active agent calling the tool.
        tool_name: Specific tool being invoked.
        args: Input parameters for the tool call.
        conversation_id: Unique conversation thread identifier.
    """
    logger.info(
        "Tool Execution Intent",
        event_stage="INTENT",
        agent_name=agent_name,
        tool_name=tool_name,
        tool_arguments=args,
        conversation_id=conversation_id or "system_default",
    )


def log_tool_outcome(
    agent_name: str,
    tool_name: str,
    status: str,
    result_summary: Any,
    conversation_id: str | None = None,
) -> None:
    """Log the actual outcome after executing a tool (OUTCOME).

    Args:
        agent_name: Name of the active agent calling the tool.
        tool_name: Specific tool invoked.
        status: Execution status ('success', 'error', 'confirmation_required').
        result_summary: Structured output or error description.
        conversation_id: Unique conversation thread identifier.
    """
    logger.info(
        "Tool Execution Outcome",
        event_stage="OUTCOME",
        agent_name=agent_name,
        tool_name=tool_name,
        status=status,
        result_summary=result_summary,
        conversation_id=conversation_id or "system_default",
    )
