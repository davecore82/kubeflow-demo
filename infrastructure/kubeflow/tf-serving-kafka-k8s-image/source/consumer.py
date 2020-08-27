#!/usr/bin/env python
import numpy as np
from kafka import KafkaConsumer, KafkaProducer
from json import dumps
from time import sleep
import request_helper

kafka_ip = "172.16.7.152"
kafka_port = "9092"
consumer = KafkaConsumer('request', group_id = 'group1', bootstrap_servers=kafka_ip + ':' + kafka_port, 
                        auto_offset_reset = 'earliest')
producer = KafkaProducer(bootstrap_servers=kafka_ip + ':' + kafka_port)
for message in consumer:
    recieved = np.fromstring(message.value, dtype = np.float32).reshape((1, 24))
    result = request_helper.send_request(recieved)
    if not result:
        continue
    producer.send('response', value=str(result))
    producer.flush()


