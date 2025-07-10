from confluent_kafka import Producer
from dotenv import load_dotenv
import json
import os

# Load environment variables from .env file
load_dotenv()

KAFKA_BROKERS = os.getenv("KAFKA_BROKERS")

conf = {
    'bootstrap.servers': KAFKA_BROKERS
}

producer = Producer(conf)

def delivery_report(err, msg):
    if err is not None:
        print(f'❌ Delivery failed: {err}')
    else:
        print(f'✅ Message delivered to {msg.topic()} [{msg.partition()}] @ offset {msg.offset()}')

# Read messages from the NDJSON file
with open("data/history.ndjson", "r") as f:
    for line in f:
        line = line.strip()
        if not line:
            continue  # skip empty lines
        try:
            msg = json.loads(line)
            producer.produce(
                topic="zabbix.items",
                value=json.dumps(msg),
                key=str(msg.get("itemid", "")),  # key is optional
                callback=delivery_report
            )
            producer.poll(0)
        except json.JSONDecodeError as e:
            print(f"⚠️ Skipping invalid JSON line: {e}")

producer.flush()
