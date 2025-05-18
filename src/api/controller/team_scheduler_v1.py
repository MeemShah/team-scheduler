from fastapi import APIRouter, status, Request, Depends, Query
from datetime import date
from ..utiils.send_data import send_data
from ..utiils.send_error import send_error
from ...dto.config import INITIAL_DATE,TEAM_PAIRS,PAIR_SEQUENCE
from ...exceptions import WeekendException,EmptyTeamListError,NotFoundError,InitialDateAfterQueryDateError
import logging
from .startup import get_controller
from .controller import Controller
router = APIRouter(
    prefix="/team/v1",
    tags=["TeamScheduler"]
)

@router.get("/{team_id}/schedule", status_code=status.HTTP_200_OK)
async def get_team(
    team_id: int,
    query_date: date = Query(default_factory=date.today),
    controller: Controller = Depends(get_controller),
    ):
    try:
        scheduled_to_work,total_working_day = controller.team_scheduler_svc.get_schedule(
            team_id,
            query_date
        )

        return send_data("Team retrieved Successful", {
            "scheduled_to_work":scheduled_to_work,
            "total_working_days": total_working_day
        })
    except EmptyTeamListError:
        return send_error("Team List empty, Add team Member first",None)
    
    except InitialDateAfterQueryDateError:
        return send_error("Initial date is after query date",None)

    except NotFoundError:
        return send_error("Team not found",None,404)

    except WeekendException:
        return send_data("Happy Weekend")

    except Exception as e:
        logging.error("Unexpected error occurred", exc_info=True)
        return send_error("Something went wrong ! we are working on it ;D",None,200)
    

@router.get("/{team_id}/details")
async def get_team(
    team_id: int,
    controller: Controller = Depends(get_controller),
):
    try:
        response = controller.team_scheduler_svc.get_team(team_id)

        return send_data("Team retrieved successfully", {
            "name": response.team_name,
            "lead": response.team_lead,
            "working_days": response.working_days,
            "initial_start_date": str(response.initial_start_date),
            "pairs": response.team_pairs
        })

    except NotFoundError:
        return send_error("Team not found",None,404)

    except WeekendException:
        return send_data("Happy Weekend")

    except Exception as e:
        logging.error("Unexpected error occurred while fetching team details", exc_info=True)
        return send_error("Something went wrong! We are working on it ;D", None, 500)
    

@router.get("/{team_id}/schedule/week")
async def get_team(
    team_id: int,
    query_date: date = Query(default_factory=date.today),
    controller: Controller = Depends(get_controller),
):
    try:
        response = controller.team_scheduler_svc.get_weekly_schedule(team_id, query_date)
        return send_data("Team retrieved successfully",response)
    
    except EmptyTeamListError:
        return send_error("Team List empty, Add team Member first",None)

    except NotFoundError:
        return send_error("Team not found",None,404)

    except WeekendException:
        return send_data("Happy Weekend")

    except Exception as e:
        logging.error("Unexpected error occurred while fetching team details", exc_info=True)
        return send_error("Something went wrong! We are working on it ;D", None, 500)

