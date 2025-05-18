import logging
from contextlib import contextmanager
from sqlmodel import SQLModel, create_engine, Session
from sqlalchemy.exc import SQLAlchemyError
from ..config.config import DBConfig

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Database:
    def __init__(self, config: DBConfig):
        self.config = config
        self._engine = None
        self._setup_engine()
        #self._initialize_schema()

    def _setup_engine(self):
        try:
            db_url = (f"postgresql+psycopg2://{self.config.user}:{self.config.password}"
                      f"@{self.config.host}:{self.config.port}/{self.config.name}")
            connect_args = {"sslmode": "require"} if self.config.enable_ssl_mode else {}
            
            self._engine = create_engine(db_url, connect_args=connect_args, pool_pre_ping=True)
            logger.info("Database engine initialized successfully.")
        except SQLAlchemyError as e:
            logger.critical("Failed to create database engine!", exc_info=True)
            raise RuntimeError("Database connection failed.") from e

    def _initialize_schema(self):
        try:
            logger.info("Initializing database schema...")
            SQLModel.metadata.create_all(bind=self._engine)
            logger.info("Database schema initialized successfully.")
        except SQLAlchemyError as e:
            logger.critical("Schema initialization failed!", exc_info=True)
            raise RuntimeError("Failed to initialize database schema.") from e

    @contextmanager
    def get_session(self):
        session = Session(self._engine)
        try:
            yield session
            session.commit()
        except SQLAlchemyError:
            session.rollback()
            logger.error("Transaction error! Rolling back.", exc_info=True)
            raise
        finally:
            session.close()

