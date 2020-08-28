#!/usr/bin/env python
import numpy as np
from kafka import KafkaConsumer, KafkaProducer
from json import dumps
from time import sleep
import request_helper
import os

kafka_ip = os.environ['KAFKA_IP']
kafka_port = "9092"
consumer = KafkaConsumer('request', group_id = 'group1', bootstrap_servers=kafka_ip + ':' + kafka_port,
                        auto_offset_reset = 'earliest')
producer = KafkaProducer(bootstrap_servers=kafka_ip + ':' + kafka_port)
for message in consumer:
    recieved = np.fromstring(message.value, dtype = np.float32).reshape((1, 24))
    print(recieved)
    result = request_helper.send_request(recieved)
    if not result:
        continue
    producer.send('response', value=str(result))
    producer.flush()
