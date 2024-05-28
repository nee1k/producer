# Dockerfile
FROM python:3.8-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy the Python script
COPY create_kafka_events.py .

# Ensure the logs directory exists in the Docker image
RUN mkdir -p /app/logs

# Command to run the Kafka events script
CMD ["python", "create_kafka_events.py"]
