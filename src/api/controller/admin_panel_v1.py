from fastapi import APIRouter, status, Request, Depends, Query, Form
from datetime import date
from ..utiils.send_data import send_data
from ..utiils.send_error import send_error
from ...dto.config import INITIAL_DATE,TEAM_PAIRS,PAIR_SEQUENCE
from ...exceptions import WeekendException,InternalServerError,NotFoundError,InitialDateAfterQueryDateError
from .startup import get_controller
from .controller import Controller
from ...dto.teams import GetTeamsReq as get_teams_req
from ...logger.logger import logging as logger
from typing import Optional
from pydantic import BaseModel
from typing import Annotated

class CreateTeamReq(BaseModel):
    teamName: str
    teamLead: str
    initialStartingDate: date

class GetTeamsReq(BaseModel):
    team_name: Optional[str] = None
    team_lead: Optional[str] = None
    page: int =1
    limit: int =10
    sort_by: str = "id"
    sort_order: str = "DESC"


router = APIRouter(
    prefix="/admin/v1/team",
    tags=["AdminPanel"]
)


@router.post("/")
async def create_team(
    req: Annotated[CreateTeamReq, Form()],
    controller: Controller = Depends(get_controller),                      
):
    try:
        controller.team_scheduler_svc.create_team(req.teamName, req.teamLead, req.initialStartingDate)
        return send_data("Team Created Succesful")
    
    except Exception:
        return send_error("failed to create new team")

@router.get("/")
async def get_teams(
    req: Annotated[GetTeamsReq, Query()],
    controller: Controller = Depends(get_controller),                      
):
    try:
        response = controller.team_scheduler_svc.get_teams(get_teams_req(
            team_name=req.team_name,
            team_lead=req.team_lead,
            page=req.page,
            limit=req.limit,
            sortBy=req.sort_by,
            sortOrder=req.sort_order
        ))
        return send_data("Successfully fetch items", response)
    
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
        # Call the service to create the team pair
        controller.team_scheduler_svc.add_team_pair(member_1, member_2, teamId)
        return send_data("Team Created Successfully")
    
    except Exception as e:
        logger.error(f"Error while adding pairs: {e}", exc_info=True)
        return send_error("Failed to create new team")