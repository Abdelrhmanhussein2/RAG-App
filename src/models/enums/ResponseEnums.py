from enum import Enum

class ResponseStatus(Enum):
    FILE_VALIDATED_SUCCESS = "File validated successfully."
    FILE_VALIDATION_FAILED = "File validation failed."
    FILE_SIZE_EXCEEDED = "File size exceeds the maximum limit."
    PROCESSING_SUCCESS = "File processed successfully."
    PROCESSING_FAILED = "File processing failed."
    UPLOAD_FAILED = "File upload failed."
    UPLOAD_SUCCESS = "File uploaded successfully."