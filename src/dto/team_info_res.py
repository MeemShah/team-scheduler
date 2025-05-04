from pydantic import BaseModel
from typing import List, Tuple
from datetime import date

class TeamInfoResponse(BaseModel):
    team_name: str
    team_lead: str
    initial_start_date: date
    team_pairs: List[Tuple[str, str]]
