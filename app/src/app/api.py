from fastapi import FastAPI
from app.models import UserModel

app = FastAPI()

@app.get("/", tags=["root"])
async def read_root() -> dict:
    return {"message": "This is root page"}

