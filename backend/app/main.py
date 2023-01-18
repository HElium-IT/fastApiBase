from fastapi import FastAPI, APIRouter
from app.api import api_v1

app = FastAPI()
app.include_router(api_v1)