from fastapi import FastAPI
from .logger.logger import configure_logger, LogLevels
from .api.routes import register_routes
from .config.config import Config
from .api.middlewares.cors import EnableCors
from .repository.db import Database
from .repository.team_repo import TeamRepo
from .repository.team_member_repo import TeamMemberRepo
from .api.controller.startup import configure_startup
from .team_scheduler_svc.team_scheduler import TeamScheduler

config = Config()
db= Database(config.db_config)
team_repo= TeamRepo(db)
team_member_repo= TeamMemberRepo(db)

scheduler = TeamScheduler(cnf=config, team_repo=team_repo, team_member_repo=team_member_repo)
configure_logger(LogLevels.info)

app = FastAPI()
app = EnableCors(app)
configure_startup(app,config,scheduler)

register_routes(app)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, port=config.http_port)
