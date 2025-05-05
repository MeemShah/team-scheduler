from fastapi.responses import JSONResponse
from .send_json import send_json
from typing import Any

def send_data(msg: str, data: Any = None) -> JSONResponse:
    return send_json(msg, data, status_code=200)