from sqlmodel import select
from sqlmodel import Session
from sqlalchemy.orm import selectinload
from ..database.db import Database
from ..entites.teams import Teams
from ..dto.team_info_res import TeamInfoResponse
from ..logger.logger import logging

class TeamRepo:
    def __init__(self, db: Database):
        self._db = db

    def get_team(self, team_id: int) -> TeamInfoResponse:
        try:
            with self._db.get_session() as session:
                query = (
                    select(Teams)
                    .where(Teams.id == team_id)
                    .options(selectinload(Teams.team_member_pairs))
                )
                team = session.exec(query).first()

                if not team:
                    logging.info(f"team id not found {team_id}")
                    return None

                return TeamInfoResponse(
                    team_name=team.team_name,
                    team_lead=team.team_lead,
                    initial_start_date=team.initial_start_date,
                    team_pairs=[(pair.member_1, pair.member_2) for pair in (team.team_member_pairs or [])]
                )
            
        except Exception as e:
            logging.error(f"Error fetching team with ID {team_id}: {e}")
            return None
