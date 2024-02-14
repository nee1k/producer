#!/usr/bin/env python
import json
import os
import socket
from confluent_kafka import Producer


def delivery_callback(err, msg):
    if err:
        print('ERROR: Message failed delivery: {}'.format(err))
    else:
        print("Produced event to topic {topic}: key = {key} value = {value}".format(
            topic=msg.topic(), key=msg.key(), value=msg.value()))


if __name__ == '__main__':
    conf = {'bootstrap.servers': 'localhost:29092',
            'client.id': socket.gethostname()}

    producer = Producer(conf)

    topic = "cpu"
    volume_mount_path = '/app/logs'
    for root, dirs, files in os.walk(volume_mount_path):
        for filename in files:
            file_path = os.path.join(root, filename)
            print(f"Reading {file_path}...")
            with open(file_path, 'r') as file:
                try:
                    content = json.load(file)
                    for data in content:
                        data_to_send = json.dumps(data).encode('utf-8')  # Serialize and encode the entry dictionary
                        print(data_to_send)
                        producer.produce(topic, value=data_to_send, callback=delivery_callback)
                        producer.poll(0)

                except json.JSONDecodeError:
                    print(f"Error decoding JSON from file {file_path}")

    # Block until the messages are sent.
    producer.poll(10000)
    producer.flush()
