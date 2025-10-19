from enum import Enum, auto



class Status(Enum):
    """
    Represents the outcome or state of an operation.
    Used for explicit status reporting.
    """
    OK = auto()
    ERROR = auto()
    TIMEOUT = auto()
    INVALID_ARGUMENT = auto()
    NOT_FOUND = auto()
    BUSY = auto()

    def is_ok(self) -> bool:
        """Returns True if the status indicates success."""
        return self == Status.OK

    def is_error(self) -> bool:
        """Returns True if the status indicates any failure or exceptional condition."""
        _ERROR_STATUSES = {Status.ERROR, Status.TIMEOUT, Status.INVALID_ARGUMENT}
        return self in _ERROR_STATUSES

    def describe(self) -> str:
        """Returns a human-readable description of the status."""
        descriptions = {
            Status.OK: "Operation completed successfully.",
            Status.ERROR: "An unspecified error occurred.",
            Status.TIMEOUT: "The operation timed out.",
            Status.INVALID_ARGUMENT: "Invalid argument was provided.",
            Status.NOT_FOUND: "Requested item was not found.",
            Status.BUSY: "The system is busy and cannot process the request.",
        }
        return descriptions.get(self, "Unknown status.")

    def __str__(self):
        """Returns a human-readable representation of the status."""
        return self.describe()
