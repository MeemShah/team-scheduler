from typing import List, Optional
from datetime import date
from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import Column, JSON
from sqlalchemy.orm import relationship


class Teams(SQLModel, table=True):
    __tablename__ = "teams"

    id: Optional[int] = Field(default=None, primary_key=True)
    team_name: str
    team_lead: str
    working_days_json: List[str] = Field(
        sa_column=Column(JSON), 
        default_factory=list
    )
    initial_start_date: date

    team_member_pairs: List["TeamMemberPair"] = Relationship(
        back_populates="team",
        sa_relationship=relationship(
            "TeamMemberPair",
            back_populates="team",
            order_by=lambda: TeamMemberPair.id,
            lazy="selectin"
        )
    )


class TeamMemberPair(SQLModel, table=True):
    __tablename__ = "team_member_pairs"

    id: Optional[int] = Field(default=None, primary_key=True)
    member_1: str
    member_2: str

    team_id: int = Field(default=None, foreign_key="teams.id")
    team: Optional[Teams] = Relationship(back_populates="team_member_pairs")



