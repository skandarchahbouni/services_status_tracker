from fastapi import APIRouter
from datetime import datetime
from db.mongodb import services_status_history_collection
from db.dragonflydb import dragonfly_client
import time
from pydantic import BaseModel
from datetime import datetime
from bson import ObjectId


router = APIRouter()

@router.get("/mock-data/realtime-status-and-sla", tags=["Mock data dashboard"])
def mock_status():
    return [
        {"service": "SaaS", "status": "UP", "downtime": 10.15},
        {"service": "IaaS", "status": "DOWN", "downtime": 30},
        {"service": "PaaS", "status": "DEGRADED", "downtime": 100},
        {"service": "BaaS", "status": "MAINTENANCE", "downtime": 45},
    ]

@router.get("/mock-data/status-history", tags=["Mock data dashboard"])
def mock_status_history():
    return [
    {
        "time": "2024-02-29 8:00:00",
        "SaaS": "UP"
    },
    {
        "time": "2024-02-29 8:30:00",
        "SaaS": "DOWN",
    },
    {
        "time": "2024-02-29 9:00:00",
        "SaaS": "UP",
    },
    {
        "time": "2024-02-29 9:15:00",
        "SaaS": "UP",
    },
    {
        "time": "2024-02-29 9:30:00",
        "SaaS": "UP",
    },
    {
        "time": "2024-02-29 10:00:00",
        "SaaS": "DOWN",
    },
    {
        "time": "2024-02-29 10:30:00",
        "SaaS": "MAINTENANCE",
    }
    ]


@router.get("/realtime-status-and-sla", tags=["Real data dashboard"])
def status():
    # SaaS
    output = []
    services = ["SaaS"]
    for service in services:
        row = {}
        row["service"] = service
        row["status"] = dragonfly_client.hget(f"status:{service}", "status")
        downtime = dragonfly_client.get(f"downtime:{service}")
        if downtime:
            downtime = int(downtime)
        else:
            downtime = 0
        if row["status"] == "DOWN":
            current_time_unix = int(time.time())
            downtime += current_time_unix - int(dragonfly_client.hget(f"status:{service}", "timestamp"))
        row["downtime"] = downtime
        output.append(row)
    return output


class StatusHistoryModel(BaseModel):
    service: str
    status: str
    timestamp: datetime

    class Config:
        allow_population_by_field_name = True
        json_encoders = {ObjectId: str}
        orm_mode = True

@router.get("/status-history/{service}", tags=["Real data dashboard"])
def status_history(service: str):
    docs = services_status_history_collection.find({"service": service}).sort("timestamp", 1)
    return [StatusHistoryModel(**doc) for doc in docs]