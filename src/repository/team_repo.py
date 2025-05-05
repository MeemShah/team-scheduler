from sqlmodel import select
from sqlmodel import Session
from sqlalchemy.orm import selectinload
from ..database.db import Database
from ..entites.teams import Teams
from ..dto.teams import TeamInfoResponse, TeamCreationRequest,GetTeamsReq
from ..logger.logger import logging
from ..exceptions import InternalServerError
from typing import List
from .query_builder import TeamQueryBuilder

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
    
    def create(self, req: TeamCreationRequest) -> Teams:
        try:
            with self._db.get_session() as session:
                new_team = Teams(
                    team_name=req.team_name,
                    team_lead=req.team_lead,
                    initial_start_date=req.initial_start_date
                )
                session.add(new_team)
                session.commit()
                session.refresh(new_team)

                return new_team
            
        except Exception as e:
            logging.error(f"Failed to create team. Error: {e}")
            raise InternalServerError()
    
    def get_teams(self, req: GetTeamsReq) -> List[TeamInfoResponse]:
            try:
                with self._db.get_session() as session:
                    query = (
                        TeamQueryBuilder(session)
                        .filter_by_name(req.team_name)
                        .filter_by_lead(req.team_lead)
                        .sort_by(req.sortBy, req.sortOrder)
                        .paginate(req.page, req.limit)
                    )
                    teams= query.exec()
                    return [TeamInfoResponse.from_orm(team).dict(exclude={"team_pairs"}) for team in teams]

            except Exception as e:
                logging.error(f"Failed to fetch teams: {e}")
                raise InternalServerError()
            