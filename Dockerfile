FROM python:3.9
WORKDIR /app
COPY . /app
RUN pip install confluent-kafka
RUN chmod u+x main.py
CMD ["python", "./main.py"]