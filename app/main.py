from fastapi import FastAPI
import uvicorn
from app.db import create_table
import app.routers.user as user

app = FastAPI()

app.include_router(user.router, tags=["users"])
# app.include_router(user.router, prefix="/users", tags=["users"])

@app.on_event("startup")
async def startup_event():
    create_table()

if __name__ == '__main__':
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
    print("localhost:8000/docs")
