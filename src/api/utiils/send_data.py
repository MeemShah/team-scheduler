from fastapi.responses import JSONResponse
from .send_json import send_json

def send_data(msg: str, data: dict = None) -> JSONResponse:
    return send_json(msg, data, status_code=200)