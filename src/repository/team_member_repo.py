from sqlmodel import select
from sqlmodel import Session
from sqlalchemy.orm import selectinload
from ..database.db import Database
from ..entites.teams import Teams


class TeamMemberRepo:
    def __init__(self, db: Database):
        self._db = db