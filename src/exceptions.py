from fastapi import HTTPException, status

class TeamSchedulerError(HTTPException):
    """Base exception for team scheduler-related errors."""
    pass

class WeekendException(TeamSchedulerError):
    def __init__(self):
        message = "Happy Weekend"
        super().__init__(status_code=200, detail=message)

class InitialDateAfterQueryDateError(TeamSchedulerError):
    def __init__(self):
        message = (
            "The initial date is after the query date. "
            "Please provide a valid date range."
        )
        super().__init__(status_code=400, detail=message)

class InternalServerError(HTTPException):
    def __init__(self, detail: str = "Internal server error"):
        super().__init__(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=detail)

class NotFoundError(TeamSchedulerError):
    def __init__(self, message: str = "Info Not Found"):
        super().__init__(status_code=404, detail=message)

class EmptyTeamListError(TeamSchedulerError):
    def __init__(self, message: str = "Team list empty"):
        super().__init__(status_code=404, detail=message)