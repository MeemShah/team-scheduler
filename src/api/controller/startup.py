from fastapi import FastAPI, Request
from src.api.controller.controller import Controller
from src.team_scheduler_svc.team_scheduler import TeamScheduler
from ...config.config import Config
from ...database.db import Database
from ...repository.team_repo import TeamRepo
from ...repository.team_member_repo import TeamMemberRepo

def configure_startup(app: FastAPI):
    @app.on_event("startup")
    def startup_event():
        config = Config()
        db = Database(config.db_config)

        team_repo = TeamRepo(db)
        team_member_repo = TeamMemberRepo(db)
        
        scheduler = TeamScheduler(db=db, team_repo=team_repo, team_member_repo=team_member_repo)
        controller = Controller(team_svc=scheduler)

        app.state.controller = controller

def get_controller(request: Request) -> Controller:
    return request.app.state.controller
