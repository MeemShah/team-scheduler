import os
from dotenv import load_dotenv

class Config:
    def __init__(self):
        load_dotenv()  # Load environment variables from .env file

        self.mode = os.getenv("MODE")
        self.service_name = os.getenv("SERVICE_NAME")
        self.http_port = int(os.getenv("HTTP_PORT"))   
        
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