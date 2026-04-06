from fastapi import FastAPI, HTTPException, Request

from fastapi.responses import JSONResponse

app = FastAPI()

# in-memory DB
items_db = { 1: {"id": 1, "name": "Item 1"}, 2: {"id": 2, "name": "Item 2"}}

# Endpoint with HTTPException
@app.get("/items/{item_id}")
async def read_item(item_id: int):
    if item_id not in items_db:
        raise HTTPException(status_code=404, detail="Item not found")
    return items_db[item_id]

# Global Exception Handler
# Endpoint with custom exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"message": "An internal error occurred. Please try again later"},
    )
# Specific handler for ValueError (422 Error)
@app.exception_handler(ValueError)
async def value_error_handler(request: Request, exc: ValueError):
    return JSONResponse(
        status_code=422,
        content={
            "message": "Invalid value provided. Please try again",
            "detail": str(exc),},
    )

# Test Enpoint
@app.get("/test-value-error")    
async def test_value_error():
    raise ValueError("This is a test value error")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
