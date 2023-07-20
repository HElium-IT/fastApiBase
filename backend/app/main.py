from fastapi import FastAPI
from app.api import api_v1
from app.core.startup import startup

app = FastAPI()
app.include_router(api_v1)


@app.on_event("startup")
def run_startup():
    startup()
