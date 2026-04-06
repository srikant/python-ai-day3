from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel, Field
from typing import Dict, List

app = FastAPI()

# in-memory DB
alerts_db: Dict[int, Dict] = {}

counter = 1
# Pydantic model for alert creation
class AlertCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=50)
    severity: int = Field(..., ge=1, le=5)
    message: str = Field(..., min_length=1)

class AlertResponse(BaseModel):
    id: int
    name: str
    severity: int
    message: str

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    if exc.status_code == 404:
        return JSONResponse(
            status_code=exc.status_code,
            content={"error": "Not Found", "detail": exc.detail},
        )
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": "Bad Request", "detail": exc.detail},
    )
# Global exception handler for validation errors
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = []
    for error in exc.errors():
        field = ".".join(str(p) for p in error["loc"])
        errors.append({
            "field": error["msg"]
        })
    return JSONResponse(
        status_code=422,
        content={"errors": errors},
    )

# Global exception handler for all other exceptions
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    print(f"Error: {exc}")
    return JSONResponse(
        status_code=500,
        content={"message": "An internal error occurred. Please try again later."},
    )

# Test endpoint
# Endpoint to create an alert
@app.post("/alerts")
async def create_alert(alert: AlertCreate):
    alert_id = len(alerts_db) + 1
    alerts_db[alert_id] = alert.dict()
    return {"message": "Alert created successfully", "alert_id": alert_id}

# Endpoint to get an alert
@app.get("/alerts/{alert_id}")
async def get_alert(alert_id: int):
    if alert_id not in alerts_db:
        raise HTTPException(status_code=404, detail="Alert not found")
    return alerts_db[alert_id]


@app.get("/test-validation-error")
async def test_validation_error():
    raise RequestValidationError([{"type": "string_too_short", "loc": ("name",), "msg": "String should have at least 1 character", "input": ""}])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)