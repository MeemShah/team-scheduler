from fastapi import APIRouter, status, Request
from fastapi import Path
from datetime import date
from ...team_scheduler.team_scheduler import TeamScheduler
from ..utiils.send_data import send_data
from ..utiils.send_error import send_error
from ...dto.config import INITIAL_DATE,TEAM_PAIRS
from ...exceptions import InitialDateAfterTodayError,WeekendError,InternalServerError
import logging

router = APIRouter(
    prefix="/team-pair",
    tags=["TeamScheduler"]
)

@router.get("/today", status_code=status.HTTP_200_OK)
async def get_team():
    try:
        today = date.today()
        teamScheduler=TeamScheduler()
        pair, total_working_days = teamScheduler.get_todays_working_pair(
            INITIAL_DATE, today, TEAM_PAIRS
        )

        return send_data("Team retrieved Successful", {
            "team_member": pair,
            "total_working_days": total_working_days
        })

    except InitialDateAfterTodayError as e:
        return send_data("Initial date after todays date")

    except WeekendError:
        return send_data("Happy Weekend")

    except Exception as e:
        logging.error("Unexpected error occurred", exc_info=True)
        return send_error("Something went wrong ! we are working on it ;D",None,200)
    

@router.get("/{day_date}", status_code=status.HTTP_200_OK)
async def get_team(
   day_date: date = Path(..., example=date.today())
    ):
    try:
        teamScheduler=TeamScheduler()
        pair, total_working_days = teamScheduler.get_todays_working_pair(
            INITIAL_DATE, day_date, TEAM_PAIRS,
        )

        return send_data("Team retrieved Successful", {
            "team_member": pair,
            "total_working_days": total_working_days
        })

    except InitialDateAfterTodayError as e:
        return send_data("Whoa there, time traveler! Your initial date is in the future. Try picking something from this timeline.")

    except WeekendError:
        return send_data("Happy Weekend")

    except Exception as e:
        logging.error("Unexpected error occurred", exc_info=True)
        return send_error("Something went wrong",None,200)