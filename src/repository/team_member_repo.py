from sqlmodel import select, Session
from sqlalchemy.orm import selectinload
from .db import Database
from ..entites.teams import TeamMemberPair, Teams
from ..dto.teams import AddPairRequest
from ..logger.logger import logging
from ..exceptions import InternalServerError, NotFoundError

class TeamMemberRepo:
    def __init__(self, db: Database):
        self._db = db

    def add_pair(self, req: AddPairRequest) -> TeamMemberPair:
        try:
            with self._db.get_session() as session:
                # Check if the team exists
                team_exists = session.exec(
                    select(Teams).where(Teams.id == req.team_id)
                ).first()
                if not team_exists:
                    logging.warning(f"Team ID {req.team_id} does not exist.")
                    raise NotFoundError(f"Team with id {req.team_id} not found")

                # Create a new team member pair
                new_pair = TeamMemberPair(
                    member_1=req.member_1,
                    member_2=req.member_2,
                    team_id=req.team_id
                )
                session.add(new_pair)
                session.commit()
                session.refresh(new_pair)

                return new_pair

        except NotFoundError:
            raise NotFoundError()

        except Exception as e:
            logging.error(f"Failed to create team member pair. Error: {e}", exc_info=True)
            raise InternalServerError()