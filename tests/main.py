from kafka_consumer.zabbix import consume_msg
import json
import os


file_path = os.path.join(os.path.dirname(__file__), "history.ndjson")

if __name__ == "__main__":
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip():
                try:
                    data = json.loads(line)
                    consume_msg(msg=data)
                except json.JSONDecodeError as e:
                    print(f"Error decoding line: {e}")