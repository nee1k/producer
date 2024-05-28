# Kafka Events Producer

This project demonstrates how to create and produce Kafka events from data stored in a Docker volume. The project involves two main steps:

1. Creating logs and storing them in a Docker volume.
2. Starting a Kafka service and producing the logs as Kafka events.

## Prerequisites

- Docker
- Docker Compose

## Setup

### Step 1: Create Docker Volume and Store Logs

1. Create a Docker volume named `icicle`.
2. Run the `create_logs.py` script to store `cpu.json` and `metadata.json` in the Docker volume.

```bash
# Create the Docker volume
docker volume create icicle

# Build the Docker image
docker-compose build

# Run the create_logs.py script
docker-compose up producer

```

# Start Kafka and Zookeeper services
```bash
docker-compose up kafka zoo1
```

# Run the create_kafka_events.py script
```bash
docker-compose run producer
```