"""Python wrapper for the OpenDota API."""

from .client import OpenDota
from .constants import DotaConstants, dota_constants
from .exceptions import (
    OpenDotaAPIError,
    OpenDotaError,
    OpenDotaNotFoundError,
    OpenDotaRateLimitError,
    ReplayNotAvailableError,
)
from .fantasy import FANTASY

__version__ = "7.40.3"
__all__ = [
    "OpenDota",
    "DotaConstants",
    "dota_constants",
    "FANTASY",
    "OpenDotaError",
    "OpenDotaAPIError",
    "OpenDotaNotFoundError",
    "OpenDotaRateLimitError",
    "ReplayNotAvailableError",
]
