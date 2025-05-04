from typing import List, Optional
from datetime import date
from sqlmodel import SQLModel, Field, Relationship

class Teams(SQLModel, table=True):
    __tablename__ = "teams"

    id: Optional[int] = Field(default=None, primary_key=True)
    team_name: str
    team_lead: str
    initial_start_date: date

    team_member_pairs: List["TeamMemberPair"] = Relationship(back_populates="team")


class TeamMemberPair(SQLModel, table=True):
    __tablename__ = "team_member_pairs"

    id: Optional[int] = Field(default=None, primary_key=True)
    member_1: str
    member_2: str

    team_id: int = Field(default=None, foreign_key="teams.id")
    team: Optional[Teams] = Relationship(back_populates="team_member_pairs")



