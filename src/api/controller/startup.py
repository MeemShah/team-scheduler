from fastapi import FastAPI, Request
from src.api.controller.controller import Controller
from src.team_scheduler_svc.team_scheduler import TeamScheduler
from ...config.config import Config

def configure_startup(app: FastAPI,cnf: Config , scheduler: TeamScheduler):
    @app.on_event("startup")
    def startup_event():
        controller = Controller(cnf=cnf,team_svc=scheduler)
        app.state.controller = controller

def get_controller(request: Request) -> Controller:
    return request.app.state.controller
