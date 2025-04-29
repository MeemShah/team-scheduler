from fastapi import FastAPI
from src.api.controller.team_scheduler_controller import router as team_scheduler_router

def register_routes(app: FastAPI):
    app.include_router(team_scheduler_router)