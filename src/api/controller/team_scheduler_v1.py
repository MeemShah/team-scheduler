from fastapi import APIRouter, status, Request, Depends, Query
from fastapi import Path
from datetime import date
from ...team_scheduler.team_scheduler import TeamScheduler
from ..utiils.send_data import send_data
from ..utiils.send_error import send_error
from ...dto.config import INITIAL_DATE,TEAM_PAIRS,PAIR_SEQUENCE
from ...exceptions import InitialDateAfterTodayError,WeekendError,InternalServerError
import logging
from .startup import get_controller
from .controller import Controller
router = APIRouter(
    prefix="/team/v1",
    tags=["TeamScheduler"]
)

@router.get("/{team_id}", status_code=status.HTTP_200_OK)
async def get_team(
    team_id: int,
    query_date: date = Query(default_factory=date.today),
    controller: Controller = Depends(get_controller),
    ):
    try:
        response = controller.team_scheduler_svc.fetch_team_member_pairs(
            team_id,
            query_date
        )

        return send_data("Team retrieved Successful", {
            "team_name":response.team_name,
            "team_lead":response.team_lead,
            "members":response.team_pairs,
            "scheduled_to_work":response.todays_working_pair,
            "total_working_days": response.total_working_days
        })


    except WeekendError:
        return send_data("Happy Weekend")

    except Exception as e:
        logging.error("Unexpected error occurred", exc_info=True)
        return send_error("Something went wrong ! we are working on it ;D",None,200)
    