from fastapi import FastAPI, APIRouter
from app.api import api_router as main_router

app = FastAPI(prefix='/api')
app.include_router(main_router)


utils_router = APIRouter(prefix="/utils")
app.include_router(utils_router)

@utils_router.get('/healthchecker')
def root():
    return {'status': 'Api is up and running'}