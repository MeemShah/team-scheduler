from fastapi import APIRouter, Depends, Form
from datetime import date
from ..utiils.send_data import send_data
from ..utiils.send_error import send_error
from ...exceptions import NotFoundError
from .startup import get_controller
from .controller import Controller
from ...dto.teams import GetTeamsReq as GetTeamsReq
from ...logger.logger import logging as logger
from typing import Optional
from pydantic import BaseModel, Field
from typing import Annotated, List

class CreateTeamReq(BaseModel):
    teamName: str
    teamLead: str
    working_days: List[str] = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
    initialStartingDate: date

class GetTeams(BaseModel):
    teamName: Optional[str] = None
    teamLead: Optional[str] = None
    page: int = 1
    limit: int = 10
    sortBy: str = Field("id", alias="sort_by")
    sortOrder: str = Field("DESC", alias="sort_order")

router = APIRouter(
    prefix="/admin/v1/team",
    tags=["AdminPanel"]
)

@router.post("/")
async def create_team(
    req: CreateTeamReq,
    controller: Controller = Depends(get_controller),
):
    try:
        controller.team_scheduler_svc.create_team(
            req.teamName, req.teamLead, req.initialStartingDate, req.working_days
        )
        return send_data("Team Created Successfully")
    except Exception:
        return send_error("Failed to create new team")

@router.get("/")
async def get_teams(
    req: GetTeams = Depends(),
    controller: Controller = Depends(get_controller),
):
    try:
        response = controller.team_scheduler_svc.get_teams(
            GetTeamsReq(
                team_name=req.teamName,
                team_lead=req.teamLead,
                page=req.page,
                limit=req.limit,
                sortBy=req.sortBy,
                sortOrder=req.sortOrder,
            )
        )
        return send_data("Successfully fetched items", response)
    except Exception as e:
        logger.error(f"Error while fetching teams: {e}", exc_info=True)
        return send_error("Internal server error", None, 500)

@router.post("/team-pairs")
async def add_team_pairs(
    teamId: int = Form(...),
    member_1: str = Form(...),
    member_2: str = Form(...),
    controller: Controller = Depends(get_controller),
):
    try:
        controller.team_scheduler_svc.add_team_pair(member_1, member_2, teamId)
        return send_data("Team Created Successfully")
    except NotFoundError:
        return send_error("Team ID Not Found")
    except Exception as e:
        logger.error(f"Error while adding pairs: {e}", exc_info=True)
        return send_error("Failed to create new team")