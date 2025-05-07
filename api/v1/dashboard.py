from fastapi import APIRouter
from datetime import datetime, timezone
from collections import defaultdict
from db.mongodb import services_status_history_collection
from db.dragonflydb import dragonfly_client
import time

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
        "SaaS": "UP",
        "IaaS": "UP"
    },
    {
        "time": "2024-02-29 8:15:00",
        "IaaS": "UP"
    },
    {
        "time": "2024-02-29 8:30:00",
        "SaaS": "DOWN",
    },
    {
        "time": "2024-02-29 8:45:00",
        "IaaS": "DEGRADED"
    },
    {
        "time": "2024-02-29 9:00:00",
        "SaaS": "UP",
    },
    {
        "time": "2024-02-29 9:15:00",
        "SaaS": "UP",
        "IaaS": "DOWN"
    },
    {
        "time": "2024-02-29 9:30:00",
        "SaaS": "UP",
        "IaaS": "DOWN"
    },
    {
        "time": "2024-02-29 10:00:00",
        "SaaS": "DOWN",
        "IaaS": "DOWN"
    },
    {
        "time": "2024-02-29 10:30:00",
        "SaaS": "MAINTENANCE",
        "IaaS": "DOWN"
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


@router.get("/status-history/{service}/{panel}", tags=["Real data dashboard"])
def status_history(service: str, panel: str):
    docs = services_status_history_collection.find({"service": service}).sort("timestamp", 1)
    # Group statuses by timestamp
    grouped = defaultdict(dict)
    for doc in docs:
        ts = datetime.fromisoformat(str(doc["timestamp"]))
        service = doc["service"]
        status = doc["status"]
        grouped[ts][service] = status
    # Convert to desired format
    result = []
    all_services = set()
    for ts, services in grouped.items():
        entry = {"timestamp": ts}
        entry.update(services)
        all_services.update(services.keys())
        result.append(entry)    
    current_time = datetime.now(timezone.utc)
    last_row = {"timestamp": current_time}
    if panel != "table":
        for service in all_services:
            last_row[service] = None
        result.append(last_row)
    return result