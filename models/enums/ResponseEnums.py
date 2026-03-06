from enum import Enum

class ResponseStatus(Enum):
    FILE_VALIDATED_SUCCESS = "File validated successfully."
    FILE_VALIDATION_FAILED = "File validation failed."
    FILE_SIZE_EXCEEDED = "File size exceeds the maximum limit."
    