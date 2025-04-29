from fastapi.responses import JSONResponse
from .send_json import send_json

def send_error(msg: str, data: dict = None, status_code: int = 400) -> JSONResponse:
    return send_json(msg, data, status_code=status_code)