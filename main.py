from __future__ import annotations
from fastapi import Request, FastAPI
from database import write_event
import uvicorn
from multiprocessing import Process
import json

process_pool: list[Process] = []

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "hello from WWAI!"}


@app.post("/ingest")
async def ingest_event(request: Request):
    body = await request.json()
    write_event(json.dumps(body))
    return {"message": "thank you for feeding data"}

if __name__ == "__main__":
    uvicorn.run("server:app", host="0.0.0.0", port=8000)
