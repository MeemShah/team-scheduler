from sqlmodel import select
from sqlmodel import Session
from sqlalchemy.orm import selectinload
from ..database.db import Database
from ..entites.teams import TeamMemberPair
from ..dto.teams import AddPairRequest
from ..logger.logger import logging 
from ..exceptions import InternalServerError

class TeamMemberRepo:
    def __init__(self, db: Database):
        self._db = db

    def add_pair(self, req: AddPairRequest) -> TeamMemberPair:
            try:
                with self._db.get_session() as session:
                    new_pair = TeamMemberPair(
                        member_1=req.member_1,
                        member_2=req.member_2,
                        team_id=req.team_id
                    )
                    session.add(new_pair)
                    session.commit()
                    session.refresh(new_pair)

                    logging.info(f"new team pair created pair: {new_pair}")
                    return new_pair
                
            except Exception as e:
                logging.error(f"Failed to create team. Error: {e}")
                raise InternalServerError()
    