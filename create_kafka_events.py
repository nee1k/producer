#!/usr/bin/env python
import json
import os
import socket

from confluent_kafka import Producer


def load_pname_map(file_path):
    with open(file_path, 'r') as file:
        metadata = json.load(file)

    pname_map = {}
    for plugin in metadata.get("plugins", []):
        pname_map[plugin["name"]] = plugin["pids"]

    return pname_map


# Define the get_pname function
def get_pname(pid):
    pid_map = {pid: pname for pname, pids in pname_map.items() for pid in pids}
    return pid_map.get(pid)


# Function to generate CPU events
def generate_cpu_events(data):
    pid = data[1]
    pname = get_pname(pid)
    ptype = 'cpu'
    server_id = 1
    wattage = data[0]  # power in Watts
    timestamp = data[2]  # timestamp

    return {"server_id": server_id,
            "plugin_name": pname,
            "type": ptype,
            "value": wattage,
            "process_id": pid,
            "timestamp": timestamp}


def delivery_callback(err, msg):
    if err:
        print('ERROR: Message failed delivery: {}'.format(err))
    else:
        print("Produced event to topic {topic}: key = {key} value = {value}".format(
            topic=msg.topic(), key=msg.key(), value=msg.value()))


if __name__ == '__main__':
    conf = {'bootstrap.servers': 'localhost:9092',
            'client.id': socket.gethostname()}

    producer = Producer(conf)

    topic = "cpu"
    volume_mount_path = '/app/logs'

    for root, dirs, files in os.walk(volume_mount_path):
        for filename in files:
            file_path = os.path.join(root, filename)
            if filename == 'metadata.json':
                pname_map = load_pname_map(filename)

            if filename == 'cpu.json':
                print(f"Reading {file_path}...")
                with open(file_path, 'r') as file:
                    try:
                        content = json.load(file)
                        for record in content:
                            for timestamp, entries in record.items():
                                for entry in entries:
                                    entry.append(timestamp)  # Add timestamp to the entry data
                                    event = generate_cpu_events(entry)
                                    data_to_send = json.dumps(event).encode('utf-8')
                                    print(data_to_send)
                                    producer.produce(topic, value=data_to_send, callback=delivery_callback)
                                    producer.poll(0)
                    except json.JSONDecodeError:
                        print(f"Error decoding JSON from file {file_path}")

    # Block until the messages are sent.
    producer.poll(10000)
    producer.flush()
