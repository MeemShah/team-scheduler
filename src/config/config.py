import os
from dotenv import load_dotenv

load_dotenv()
class DBConfig:
    def __init__(self):
        self.host = os.getenv("DB_HOST")
        self.port = int(os.getenv("DB_PORT"))
        self.name = os.getenv("DB_NAME")
        self.user = os.getenv("DB_USER")
        self.password = os.getenv("DB_PASS")
        self.max_idle_time_in_minutes = int(os.getenv("MAX_IDLE_TIME_IN_MINUTES"))
        self.enable_ssl_mode = os.getenv("ENABLE_SSL_MODE", "false").lower() == "true"

        self.validate()

    def validate(self):
        required_fields = {
            "DB_HOST": self.host,
            "DB_PORT": self.port,
            "DB_NAME": self.name,
            "DB_USER": self.user,
            "DB_PASS": self.password,
            "MAX_IDLE_TIME_IN_MINUTES": self.max_idle_time_in_minutes,
        }
        missing = [field for field, value in required_fields.items() if value is None]
        if missing:
            raise ValueError(f"Missing required DB environment variables: {', '.join(missing)}")

    def to_dict(self):
        return {
            "host": self.host,
            "port": self.port,
            "dbname": self.name,
            "user": self.user,
            "password": self.password,
            "sslmode": "require" if self.enable_ssl_mode else "disable",
        }

class Config:
    def __init__(self):


        self.mode = os.getenv("MODE")
        self.service_name = os.getenv("SERVICE_NAME")
        self.http_port = int(os.getenv("HTTP_PORT"))   
        #self.db = DBConfig()

        self.validate()

    def validate(self):
        required_fields = {
            "MODE": self.mode,
            "SERVICE_NAME": self.service_name,
            "HTTP_PORT": self.http_port,
        }
        missing = [field for field, value in required_fields.items() if value is None]
        if missing:
            raise ValueError(f"Missing required service environment variables: {', '.join(missing)}")

    def to_dict(self):
        return {
            "mode": self.mode,
            "service_name": self.service_name,
            "http_port": self.http_port,
        }