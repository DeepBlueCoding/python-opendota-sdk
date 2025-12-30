"""Models for parse job requests and status."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class ParseJobData(BaseModel):
    """Data associated with a parse job."""

    match_id: int


class ParseJob(BaseModel):
    """Represents a parse job status from the OpenDota API.

    When a job is pending/in-progress, the API returns job details.
    When a job is completed or not found, the API returns null.
    """

    id: int
    job_id: int
    type: str
    timestamp: datetime
    attempts: int
    data: ParseJobData
    next_attempt_time: Optional[datetime] = None
    priority: Optional[int] = None
    job_key: Optional[str] = None

    @property
    def match_id(self) -> int:
        """Get the match ID associated with this job."""
        return self.data.match_id

    @property
    def is_pending(self) -> bool:
        """Check if the job is still pending (not completed)."""
        return True  # If we have a ParseJob object, it's pending


class ParseJobRequest(BaseModel):
    """Response from submitting a new parse request."""

    job_id: int

    @classmethod
    def from_api_response(cls, data: dict) -> "ParseJobRequest":
        """Create from API response {"job": {"jobId": 123}}."""
        return cls(job_id=data["job"]["jobId"])


class ParseStatus(BaseModel):
    """Status update yielded during parse waiting.

    Yielded by ParseTask iteration to provide progress updates
    while waiting for a replay to be parsed.
    """

    job_id: int
    match_id: int
    elapsed: float  # Seconds since parse was requested
    attempts: int  # Number of parse attempts so far
