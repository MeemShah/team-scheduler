from fastapi import APIRouter, status, Request
from datetime import date
from ...team_scheduler.service import TeamScheduler
from ..utiils.send_data import send_data
from ..utiils.send_error import send_error
from ...dto.config import INITIAL_DATE,TEAM_PAIRS,PAIR_SEQUENCE
from ...exceptions import InitialDateAfterTodayError,WeekendError,InternalServerError
import logging

router = APIRouter(
    prefix="/team-scheduler",
    tags=["TeamScheduler"]
)

@router.get("/", status_code=status.HTTP_201_CREATED)
async def get_team():
    try:
        today = date.today()
        #today=date(2025,5,1)
        teamScheduler=TeamScheduler()
        pair, total_working_days = teamScheduler.get_todays_working_pair(
            INITIAL_DATE, today, TEAM_PAIRS, PAIR_SEQUENCE
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
        return send_error("Something went wrong",None,200)