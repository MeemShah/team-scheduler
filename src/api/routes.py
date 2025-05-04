from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from src.api.controller.team_scheduler_controller import router as team_scheduler_router
from .controller.team_scheduler_v1 import router as routes_v1

def register_routes(app: FastAPI):
    @app.get("/", response_class=FileResponse)
    def read_root():
        return FileResponse("src/static/index.html")
    
    @app.head("/")
    def head_root():
        return {"message": "Team Scheduler API is running"}

    app.mount("/static", StaticFiles(directory="src/static"), name="static")

    app.include_router(team_scheduler_router)
    app.include_router(routes_v1)
