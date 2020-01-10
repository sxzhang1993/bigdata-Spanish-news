#producer

import json
from kafka import KafkaProducer
import time

def connect_kafka_producer():
    _producer = None
    try:
        _producer = KafkaProducer(bootstrap_servers=['localhost:9092'], api_version=(0, 10), linger_ms=10)

    except Exception as ex:
        print('Exception while connecting Kafka')
        print(str(ex))
    finally:
        return _producer

def publish_message(producer_instance, topic_name, value):
    try:
        key_bytes = bytes('foo', encoding='utf-8')
        value_bytes = bytes(value, encoding='utf-8')
        producer_instance.send(topic_name, key=key_bytes, value=value_bytes)
        producer_instance.flush()
        print('Message published successfully.')
    except Exception as ex:
        print('Exception in publishing message')
        print(str(ex))

if __name__ == "__main__":
    prod = connect_kafka_producer()
    count = 0;
    for i in range(1, 291):
        with open("/home/trn/PycharmProjects/Crawling/output/output" + str(i) + ".json",'r') as load_f:
            while True:
                line = load_f.readline()
                if line:
                    r = json.loads(line)
                    publish_message(prod, 'Spanish_News', line)
                    count += 1
                    # time.sleep(1)
                    print(r)
                else:
                    break
        load_f.close()
    if prod is not None:
        prod.close()

    print(count)
