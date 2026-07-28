# app/sanitizer.py
"""PII and Sensitive Data Redaction Processor.

Scrubs sensitive data (API keys, SSNs, credit card numbers, email addresses,
OAuth tokens) from logs and memory pipelines before storage.
"""

import re
from typing import Any, ClassVar


class PIISanitizer:
    """Regex-based scrubber to scrub sensitive data from structured text and objects."""

    # Common patterns for sensitive data
    REGEX_PATTERNS: ClassVar[list[tuple[re.Pattern[str], str]]] = [
        # API Keys & Secret Tokens
        (re.compile(r"(?i)(api[_-]?key|secret[_-]?key|auth[_-]?token|bearer\s+)[=:]\s*['\"]?([A-Za-z0-9_\-\.]{16,})['\"]?"), r"\1=[REDACTED_SECRET]"),
        # Generic API Key formats (e.g. AIza..., sk-...)
        (re.compile(r"\b(AIzaSy[A-Za-z0-9_\-]{33}|sk-[A-Za-z0-9]{32,})\b"), "[REDACTED_API_KEY]"),
        # Social Security Numbers (SSN)
        (re.compile(r"\b\d{3}-\d{2}-\d{4}\b"), "[REDACTED_SSN]"),
        # Credit Card Numbers
        (re.compile(r"\b(?:\d[ -]*?){13,16}\b"), "[REDACTED_CREDIT_CARD]"),
        # Email Addresses
        (re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"), "[REDACTED_EMAIL]"),
    ]

    @classmethod
    def sanitize_text(cls, text: str) -> str:
        """Sanitize a raw string by masking all sensitive data patterns.

        Args:
            text: Raw input string.

        Returns:
            Sanitized string with sensitive terms replaced.
        """
        if not text or not isinstance(text, str):
            return text

        sanitized = text
        for pattern, replacement in cls.REGEX_PATTERNS:
            sanitized = pattern.sub(replacement, sanitized)
        return sanitized

    @classmethod
    def sanitize_dict(cls, data: dict[str, Any]) -> dict[str, Any]:
        """Recursively sanitize dictionary values.

        Args:
            data: Input dictionary.

        Returns:
            New dictionary with sanitized values.
        """
        clean_data = {}
        for key, value in data.items():
            if isinstance(value, str):
                clean_data[key] = cls.sanitize_text(value)
            elif isinstance(value, dict):
                clean_data[key] = cls.sanitize_dict(value)
            elif isinstance(value, list):
                clean_data[key] = [
                    cls.sanitize_dict(item) if isinstance(item, dict)
                    else (cls.sanitize_text(item) if isinstance(item, str) else item)
                    for item in value
                ]
            else:
                clean_data[key] = value
        return clean_data


def structlog_pii_sanitizer_processor(logger: Any, method_name: str, event_dict: dict[str, Any]) -> dict[str, Any]:
    """structlog processor function to automatically scrub event dictionaries."""
    return PIISanitizer.sanitize_dict(event_dict)
