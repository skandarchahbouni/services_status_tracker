from confluent_kafka import Consumer, KafkaException
from .utils import consume_msg
import json


conf = {
    'bootstrap.servers': 'localhost:9092', 
    'group.id': 'zabbix',
    'auto.offset.reset': 'latest',
    'enable.auto.commit': False,
    # 'auto.commit.interval.ms': 5000
}

consumer = Consumer(conf)
consumer.subscribe(['items'])


try:
    while True:
        msg = consumer.poll(0.1) 
        if msg is None:
            continue
        if msg.error():
            raise KafkaException(msg.error())
        else:
            parsed_msg = json.loads(msg.value().decode('utf-8'))
            consume_msg(msg=parsed_msg)
            consumer.commit(msg)

except KeyboardInterrupt:
    print("Stopping consumer...")
finally:
    consumer.close()