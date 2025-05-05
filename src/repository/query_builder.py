from sqlalchemy.orm import Session
from sqlalchemy import asc, desc
from ..entites.teams import Teams

class TeamQueryBuilder:
    def __init__(self, session: Session):
        self.session = session
        self.query = session.query(Teams)

    def filter_by_name(self, name: str):
        if name:
            self.query = self.query.filter(Teams.team_name.ilike(f"%{name}%"))
        return self

    def filter_by_lead(self, lead: str):
        if lead:
            self.query = self.query.filter(Teams.team_lead.ilike(f"%{lead}%"))
        return self

    def sort_by(self, field: str, order: str):
        column = getattr(Teams, field, Teams.id)
        if order.upper() == "ASC":
            self.query = self.query.order_by(asc(column))
        else:
            self.query = self.query.order_by(desc(column))
        return self

    def paginate(self, page: int, limit: int):
        offset = (page - 1) * limit
        self.query = self.query.offset(offset).limit(limit)
        return self

    def exec(self):
        return self.query.all()
