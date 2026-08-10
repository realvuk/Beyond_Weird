"""Exception hierarchy for the bweird pipeline.

Every custom exception derives from :class:`BweirdError` so callers can
catch pipeline-specific failures without swallowing programming errors.
"""

from __future__ import annotations


class BweirdError(Exception):
    """Base class for all bweird pipeline errors."""


class ConfigError(BweirdError):
    """Raised when a configuration file is missing, malformed, or invalid."""


class DataError(BweirdError):
    """Raised when an input data file violates the expected schema."""


class ParseError(BweirdError):
    """Raised when a model response cannot be parsed into the expected JSON."""


class OpenRouterError(BweirdError):
    """Base class for OpenRouter API failures."""


class RateLimitError(OpenRouterError):
    """Raised on HTTP 429 responses; carries an optional server retry hint.

    Attributes:
        retry_after: Seconds to wait before retrying, if the server sent a
            ``Retry-After`` header; otherwise ``None``.
    """

    def __init__(self, message: str, retry_after: float | None = None) -> None:
        """Initialise with the error message and optional retry hint."""
        super().__init__(message)
        self.retry_after = retry_after


class TransientAPIError(OpenRouterError):
    """Raised on retryable failures: 5xx responses, timeouts, bad payloads."""


class PermanentAPIError(OpenRouterError):
    """Raised on non-retryable failures such as authentication errors."""


class CircuitBreakerError(BweirdError):
    """Raised when the consecutive abstention threshold is reached."""

