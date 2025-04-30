from fastapi import FastAPI
from .logger.logger import configure_logger, LogLevels
from .api.routes import register_routes
from .config.config import Config
from .api.middlewares.cors import EnableCors
config = Config()

configure_logger(LogLevels.info)

app = FastAPI()
app = EnableCors(app)

register_routes(app)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, port=config.http_port)
