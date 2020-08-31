from kafka import KafkaProducer
from json import dumps
import json
from time import sleep
from kafka import KafkaConsumer
from datetime import datetime, timedelta
import numpy as np
import pandas as pd
import load_data
import preprocess

elasicsearch_address="172.16.7.59"
kafka_ip = "172.16.7.149"
kafka_port = "9092"

producer = KafkaProducer(bootstrap_servers=kafka_ip + ':' + kafka_port, retries = 5)
consumer = KafkaConsumer('response', bootstrap_servers=kafka_ip + ':' + kafka_port, auto_offset_reset = 'earliest')
closing_data = load_data.load_closing_data(elasicsearch_address)

def add_row(closing_data, date, new_data):
    closing_data.loc[pd.to_datetime(date)] = new_data
    closing_data = closing_data.sort_index()
    return closing_data

def produce(date, closing_date):
      input_tensor = load_data.get_formatted_data(closing_data, preprocessed_data, date.strftime('%Y-%m-%d'))
      producer.send('request', value=input_tensor.tostring())

def consume(date, closing_data):
      for message in consumer:
            value = eval(message.value)
            if value['prediction'] == 0:
                print("S&P 500 will close POSITIVE today")
            else:
                print("S&P 500 will close NEGATIVE today")
            date = date + timedelta(days=1)
            break 
 #           produce(date, closing_data)

date = '2021-07-31'
new_data = [11085.810059, 73333.879883, 11869.019531, 80963.719727, 19620.009766, 53020.0, 59907.740234, 42037.899902]
closing_data = add_row(closing_data, date, new_data)
preprocessed_data = preprocess.preprocess_data(closing_data)
begin_date = datetime.strptime(date,'%Y-%m-%d')
produce(begin_date, closing_data)
consume(begin_date, closing_data)


