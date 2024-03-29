from __future__ import annotations
from fastapi import Request, FastAPI
from database import write_event
from bigquery import write_event_bigquery
import uvicorn, json

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "hello from WWAI!"}


@app.post("/ingest")
async def ingest_event(request: Request):
    body = await request.json()
    write_event(json.dumps(body))
    return {"message": "thank you for feeding data"}


@app.post("/ingest-gcp")
async def ingest_event_gcp(request: Request):
    body = await request.json()
    write_event_bigquery(json.dumps(body))
    return {"message": "thank you for feeding data to GCP!"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000)
