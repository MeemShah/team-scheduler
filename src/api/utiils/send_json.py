from fastapi.responses import JSONResponse

def send_json(msg: str, data: dict = None, status_code: int = 200) -> JSONResponse:
    response = {
        "message": msg,
        "data": data
    }
    return JSONResponse(content=response, status_code=status_code)
