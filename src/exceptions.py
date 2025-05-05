from fastapi import HTTPException,status

class TeamSchedulerError(HTTPException):
    """Base exception for todo-related errors"""
    pass

class WeekendException(TeamSchedulerError):
    def __init__(self):
        message = "Happy Weekend"
        super().__init__(status_code=200, detail=message)

class InitialDateAfterQueryDateError(TeamSchedulerError):
    def __init__(self):
        message = (
            f"The initial date  is after query date )."
            "Please provide a valid date range."
        )
        super().__init__(status_code=400, detail=message)


class InternalServerError(HTTPException):
    def __init__(self, detail: str = "Internal server error"):
        super().__init__(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=detail)


class NotFoundError(TeamSchedulerError):
    def __init__(self,message: str = "Info Not Found"):
        super().__init__(status_code=404, detail=message)