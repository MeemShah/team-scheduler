from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from .controller.team_scheduler_v1 import router as routes_v1
from .controller.admin_panel_v1 import router as admin_panel_v1

def register_routes(app: FastAPI):
    @app.get("/index.html", response_class=FileResponse)
    def read_root():
        return FileResponse("src/static/index.html")
    
    # @app.get("/dashboard.html")
    # async def serve_dashboard():
    #     return FileResponse("src/static/dashboard.html")
    
    @app.get("/create-team.html")
    async def serve_dashboard():
        return FileResponse("src/static/create-team.html")
    
    @app.get("/get-teams.html")
    async def serve_dashboard():
        return FileResponse("src/static/get-teams.html")
    
    @app.get("/add-pairs.html")
    async def serve_dashboard():
        return FileResponse("src/static/add-pairs.html")
    
    @app.head("/")
    def head_root():
        return {"message": "Team Scheduler API is running"}

    app.mount("/static", StaticFiles(directory="src/static"), name="static")

    app.include_router(routes_v1)
    app.include_router(admin_panel_v1)
