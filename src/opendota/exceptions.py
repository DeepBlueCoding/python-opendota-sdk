"""Custom exceptions for the OpenDota API wrapper."""

from typing import Optional


class OpenDotaError(Exception):
    """Base exception for OpenDota API errors."""
    pass


class OpenDotaAPIError(OpenDotaError):
    """Exception raised for API errors."""

    def __init__(self, message: str, status_code: Optional[int] = None):
        self.status_code = status_code
        super().__init__(message)


class OpenDotaRateLimitError(OpenDotaAPIError):
    """Exception raised when rate limit is exceeded."""
    pass


class OpenDotaNotFoundError(OpenDotaAPIError):
    """Exception raised when resource is not found."""
    pass


class ReplayNotAvailableError(OpenDotaError):
    """Exception raised when replay URL is not available for a match.

    This typically happens when:
    - OpenDota hasn't parsed the match yet
    - The replay has expired from Valve's servers
    - The match doesn't have a replay (e.g., bot matches)

    Use wait_for_replay_url=True in get_match() to automatically
    request a reparse and wait for the replay URL.
    """

    def __init__(self, match_id: int, message: Optional[str] = None):
        self.match_id = match_id
        if message is None:
            message = (
                f"Replay URL not available for match {match_id}. "
                "Use wait_for_replay_url=True to request reparse and wait."
            )
        super().__init__(message)
