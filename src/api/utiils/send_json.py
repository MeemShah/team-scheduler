from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from typing import Any

def send_json(msg: str, data: Any = None, status_code: int = 200) -> JSONResponse:
    response = {
        "message": msg,
        "data": jsonable_encoder(data)
    }
    return JSONResponse(content=response, status_code=status_code)
