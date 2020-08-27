from kafka import KafkaProducer
from json import dumps
from time import sleep
from kafka import KafkaConsumer
import numpy as np
kafka_ip = "172.16.7.152"
kafka_port = "9092"

producer = KafkaProducer(bootstrap_servers=kafka_ip + ':' + kafka_port, retries = 5)
consumer = KafkaConsumer('response', bootstrap_servers=kafka_ip + ':' + kafka_port, auto_offset_reset = 'earliest')


def produce():
      input_tensor = np.random.rand(1, 24).astype(np.float32)
      print(input_tensor)
      producer.send('request', value=input_tensor.tostring())

def consume():
      for message in consumer:
            print (message.value)
            produce()
produce()
consume()

