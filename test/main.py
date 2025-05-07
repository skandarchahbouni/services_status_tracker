from kafka_consumer.zabbix import consume_msg
import json

if __name__ == "__main__":
    # Read and process historical metrics from an NDJSON file
    with open("/home/skandar/Downloads/poc - items/data/history.ndjson", 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip():
                try:
                    data = json.loads(line)
                    consume_msg(msg=data)
                except json.JSONDecodeError as e:
                    print(f"Error decoding line: {e}")