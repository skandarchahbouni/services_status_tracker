from db.valkey import valkey_client
from db.mongodb import services_status_history_collection
from dotenv import load_dotenv
import ast
import os
from datetime import datetime, timezone

# Load environment variables from a .env file
load_dotenv()
index = {
    50489: ["SaaS"], 
    50486: ["SaaS"], 
    50492: ["SaaS"]
}

# Maximum number of items to keep per item ID
max_items = int(os.getenv("MAX_ITEMS"))


def cumulate_downtime(service: str, duration: int):
    """
    Increment the total downtime of a service by the specified duration.
    """
    valkey_client.incrby(f"downtime:{service}", duration)


def update_service_status(service: str, status: str, timestamp: int):
    """
    Update the current status and timestamp of a service in the database.
    """
    d = {"service": service, "status": status, "timestamp": timestamp}
    print("Updating: ....", d)
    valkey_client.hset(f"status:{service}", mapping=d)
    d["timestamp"] = datetime.fromtimestamp(d["timestamp"], tz=timezone.utc)
    services_status_history_collection.insert_one(document=d)


def check_service_status(service: str, timestamp: int):
    """
    Evaluate the current status of a service (e.g., SaaS) based on recent metric values,
    and update the status if it has changed. Cumulate downtime if transitioning from DOWN.
    """
    if service == "SaaS":
        app_host = get_latest_values(itemid="50489", n=3)
        db_host  = get_latest_values(itemid="50486", n=3)
        ws_host = get_latest_values(itemid="50492", n=3)

        # If any list has less than 3 values, status is UNKNOWN
        if len(app_host) < 3 or len(db_host) < 3 or len(ws_host) < 3:
            status = "UNKNOWN"
        # If any component is fully down (max = 0), service is DOWN
        elif max(app_host) == 0 or max(db_host) == 0 or max(ws_host) == 0:
            status = "DOWN"
        else: 
            status = "UP"

    elif service == "PaaS":
        status = "from formula ..."  # Placeholder logic
    elif service == "IaaS":
        status = "from formula ..."  # Placeholder logic

    # Get previous status to detect changes
    previous = valkey_client.hgetall(f"status:{service}")
    previous_status, previous_timestamp = None, None
    if previous:
        previous_status = previous.get("status", "UNKNOWN")

    if status != previous_status:
        print(f"Updating status from: {previous_status} to {status}")
        update_service_status(service=service, status=status, timestamp=timestamp)       
        # Calculate downtime duration only if transitioning from DOWN
        if previous_status == "DOWN":
            previous_timestamp = int(previous.get("timestamp"))
            cumulate_downtime(service=service, duration=timestamp - previous_timestamp)


def consume_msg(msg: dict):
    """
    Consume a metric message and update the relevant service(s) it affects.
    """
    itemid = msg["itemid"]
    value = msg["value"]
    timestamp = int(msg["clock"])
    if itemid in index.keys():
        # Add the value to the capped list for this itemid
        push_capped_list(key=f"items:{itemid}", value=value)
        # Check and update status for all services this item belongs to
        for service in index.get(itemid, []):
            check_service_status(service=service, timestamp=timestamp)


def push_capped_list(key: str, value: str, max_items: int = max_items):
    """
    Add a new value to a Redis list and trim it to keep only the last `max_items` entries.
    """
    valkey_client.lpush(key, value)
    valkey_client.ltrim(key, 0, max_items - 1)
    result = [parse_value(item) for item in valkey_client.lrange(key, 0, -1)]
    print(f"{key}: {result}")


def parse_value(val: str):
    """
    Safely parse a string value into a Python literal (e.g., int, float).
    """
    val = val.strip()
    try:
        return ast.literal_eval(val)
    except (ValueError, SyntaxError):
        print(f"Error when parsing ... {val}")
    return val


def get_latest_values(itemid: str, n: int) -> list:
    """
    Fetch the latest `n` values for a given item ID from the capped list.
    """
    return [parse_value(item) for item in valkey_client.lrange(f"items:{itemid}", 0, n - 1)]