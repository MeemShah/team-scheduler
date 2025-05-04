from sqlmodel import select
from sqlmodel import Session
from sqlalchemy.orm import selectinload
from ..database.db import Database
from ..entites.teams import Teams
from ..dto.team_info_res import TeamInfoResponse


class TeamRepo:
    def __init__(self, db: Database):
        self._db = db

    def get_team(self, team_id: int) -> TeamInfoResponse:
        with self._db.get_session() as session:
            query = (
                select(Teams)
                .where(Teams.id == team_id)
                .options(selectinload(Teams.team_member_pairs))
            )
            team = session.exec(query).first()

            if not team:
                return None

            return TeamInfoResponse(
                team_name=team.team_name,
                team_lead=team.team_lead,
                initial_start_date=team.initial_start_date,
                team_pairs=[(pair.member_1, pair.member_2) for pair in (team.team_member_pairs or [])]
            )