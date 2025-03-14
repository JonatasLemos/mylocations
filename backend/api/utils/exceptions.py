from fastapi import HTTPException, status


class NotFoundException(HTTPException):
    """Custom not found exception class"""

    def __init__(self, detail: str = "Object not found."):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)
