from pydantic import BaseModel
from typing import List, Tuple
from datetime import date
from typing import Optional

class TeamInfoResponse(BaseModel):
    id: Optional[int]=None
    team_name: str
    team_lead: str
    working_days: Optional[List[str]] = None
    initial_start_date: date
    team_pairs: Optional[List[Tuple[str, str]]] = None

    class Config:
        from_attributes = True

class TeamCreationRequest(BaseModel):
    team_name: str
    team_lead: str
    working_days: List[str]
    initial_start_date: date

class AddPairRequest(BaseModel):
    member_1: str
    member_2: str
    team_id: int

class GetTeamsReq(BaseModel):
    team_name: Optional[str] = None 
    team_lead: Optional[str] = None 
    page: int = 1
    limit: int = 10
    sortBy: str = "id"
    sortOrder: str = "DESC"

class AddWorkingDaysRequest(BaseModel):
    team_id: int 
    working_days: List[str]