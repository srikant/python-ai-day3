import asyncio
from fastapi import FastAPI

app = FastAPI()

# Sync Endpoint
@app.get("/ping")
def ping():
    return {"message": "pong"}

# Async Endpoint
@app.get("/ping-async")
async def ping_async():
    return {"message": "pong async"}

# Simulate DB Call
async def fake_db_query(user_id: int) -> dict:
    await asyncio.sleep(2)    
    return {"user_id": user_id, "name": "John Doe"}

# call this db 
@app.get("/users/{user_id}")
async def get_user(user_id: int):
    user = await fake_db_query(user_id)
    return user

@app.post("/process-image")
def process_image():    
    return {"message": "Image processed"}
# RUN SERVER

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)