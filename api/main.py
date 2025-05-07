from fastapi import FastAPI
from api.v1 import dashboard

app = FastAPI()

app.include_router(dashboard.router, prefix="/api/v1")