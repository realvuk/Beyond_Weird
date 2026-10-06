"""Minimal, retry-hardened OpenRouter chat-completions client.

All pipeline API traffic goes through :class:`OpenRouterClient.chat`, which
is wrapped by :func:`retry_on_transient` (built on `tenacity`): jittered
exponential backoff on rate limits (honouring ``Retry-After``), 5xx
responses, timeouts, and malformed payloads. Authentication failures are
permanent and are not retried.

The client always sends an explicit ``temperature`` (the pipeline uses 0.0
everywhere for reproducibility) and a fixed ``seed`` for providers that
support it.
"""

from __future__ import annotations

import logging
import os
from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, TypeVar

import requests
from dotenv import load_dotenv
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential_jitter

from bweird.errors import (
    ConfigError,
    PermanentAPIError,
    RateLimitError,
    TransientAPIError,
)

logger = logging.getLogger(__name__)

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
API_KEY_ENV_VAR = "OPENROUTER_API_KEY"

#: Fixed provider-side seed sent with every request, for providers that
#: support seeded sampling (harmless where unsupported).
DEFAULT_SEED = 20260708

_F = TypeVar("_F", bound=Callable[..., Any])


def _load_dotenv(path: Path = Path(".env")) -> None:
    """Populate ``os.environ`` from a ``KEY=value`` .env file, if one exists.

    Already-set environment variables win, so an exported key overrides the
    file. ponytail: reads .env from the cwd; run the scripts from the repo root.
    """
    load_dotenv(path, override=False)


def retry_on_transient(
    max_attempts: int = 6,
    base_delay: float = 2.0,
    max_delay: float = 90.0,
) -> Callable[[_F], _F]:
    """Decorator retrying transient API failures with jittered backoff.

    Retries :class:`RateLimitError` and :class:`TransientAPIError`; a server
    ``Retry-After`` hint on a :class:`RateLimitError` takes precedence over
    the computed exponential backoff. :class:`PermanentAPIError` and all
    non-API exceptions propagate immediately.
    """
    if max_attempts < 1:
        raise ValueError("max_attempts must be >= 1")

    backoff = wait_exponential_jitter(initial=base_delay, max=max_delay, jitter=base_delay)

    def wait(retry_state: Any) -> float:
        exc = retry_state.outcome.exception()
        if isinstance(exc, RateLimitError) and exc.retry_after is not None:
            return min(max_delay, exc.retry_after)
        return float(backoff(retry_state))

    def before_sleep(retry_state: Any) -> None:
        logger.warning(
            "%s (attempt %d/%d) -- retrying in %.1fs",
            retry_state.outcome.exception(),
            retry_state.attempt_number,
            max_attempts,
            retry_state.next_action.sleep,
        )

    tenacity_retry = retry(
        retry=retry_if_exception_type((RateLimitError, TransientAPIError)),
        stop=stop_after_attempt(max_attempts),
        wait=wait,
        before_sleep=before_sleep,
        reraise=True,
    )

    def decorator(func: _F) -> _F:
        return tenacity_retry(func)

    return decorator


@dataclass(frozen=True)
class ChatResponse:
    """Successful chat-completion result: text, serving model, token usage."""

    content: str
    model: str
    usage: Mapping[str, int] = field(default_factory=dict)


class OpenRouterClient:
    """Thin synchronous client for the OpenRouter chat-completions API."""

    def __init__(
        self,
        api_key: str | None = None,
        timeout: float = 180.0,
        session: requests.Session | None = None,
        app_url: str = "https://github.com/beyond-weird/bweird",
        app_title: str = "Beyond WEIRD benchmark",
    ) -> None:
        """Initialise the client; the key defaults to ``OPENROUTER_API_KEY``."""
        _load_dotenv()
        resolved_key = api_key or os.environ.get(API_KEY_ENV_VAR)
        if not resolved_key:
            raise ConfigError(
                f"No OpenRouter API key: pass api_key or set {API_KEY_ENV_VAR}"
            )
        self.timeout = timeout
        self._session = session or requests.Session()
        self._session.headers.update(
            {
                "Authorization": f"Bearer {resolved_key}",
                "Content-Type": "application/json",
                "HTTP-Referer": app_url,
                "X-Title": app_title,
            }
        )

    @retry_on_transient()
    def chat(
        self,
        model: str,
        messages: Sequence[Mapping[str, str]],
        temperature: float = 0.0,
        max_tokens: int = 4096,
        seed: int = DEFAULT_SEED,
    ) -> ChatResponse:
        """Run one chat completion, retrying transient failures."""
        payload: dict[str, Any] = {
            "model": model,
            "messages": list(messages),
            "temperature": temperature,
            "max_tokens": max_tokens,
            "seed": seed,
        }
        try:
            response = self._session.post(OPENROUTER_URL, json=payload, timeout=self.timeout)
        except requests.RequestException as exc:
            raise TransientAPIError(f"Network error calling {model}: {exc}") from exc

        if response.status_code == 429:
            raise RateLimitError(
                f"Rate limited on {model}", retry_after=_parse_retry_after(response)
            )
        if response.status_code in (401, 403):
            raise PermanentAPIError(
                f"Authentication failed ({response.status_code}): check {API_KEY_ENV_VAR}"
            )
        if response.status_code >= 500:
            raise TransientAPIError(f"Server error {response.status_code} on {model}")
        if response.status_code != 200:
            raise PermanentAPIError(
                f"Unexpected status {response.status_code} on {model}: {response.text[:500]}"
            )

        try:
            body = response.json()
        except ValueError as exc:
            raise TransientAPIError(f"Non-JSON response body from {model}") from exc

        # OpenRouter can return HTTP 200 with an error object (e.g. when the
        # upstream provider fails); treat that as transient.
        if isinstance(body, dict) and "error" in body:
            raise TransientAPIError(f"API error from {model}: {body['error']}")

        try:
            content = body["choices"][0]["message"]["content"]
        except (KeyError, IndexError, TypeError) as exc:
            raise TransientAPIError(f"Malformed completion payload from {model}") from exc
        if not isinstance(content, str) or not content.strip():
            raise TransientAPIError(f"Empty completion from {model}")

        usage_raw = body.get("usage") or {}
        usage = {
            str(k): int(v) for k, v in usage_raw.items() if isinstance(v, (int, float))
        }
        return ChatResponse(
            content=content, model=str(body.get("model", model)), usage=usage
        )


def _parse_retry_after(response: requests.Response) -> float | None:
    """Extract a ``Retry-After`` hint in seconds, if present and numeric."""
    header = response.headers.get("Retry-After")
    if header is None:
        return None
    try:
        return max(0.0, float(header))
    except ValueError:
        return None
