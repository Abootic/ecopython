# Enum for HTTP status codes
from dataclasses import dataclass
from enum import Enum


class StatusCode(Enum):
    SUCCESS = 200
    BAD_REQUEST = 400
    INTERNAL_SERVER_ERROR = 500

# The MessageResult class represents the metadata for the result
@dataclass(frozen=True)
class MessageResult:
    message: str = ''
    code: StatusCode = StatusCode.SUCCESS
    succeeded: bool = False

    # Auto-set succeeded based on the status code
    def __post_init__(self):
        object.__setattr__(self, 'succeeded', self.code == StatusCode.SUCCESS)

