from fastapi import FastAPI
from datetime import datetime, date
from .logger.logger import configure_logger, LogLevels
from .api.routes import register_routes


configure_logger(LogLevels.info)

app = FastAPI()

register_routes(app)
