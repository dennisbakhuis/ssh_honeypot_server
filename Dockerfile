FROM python:3.11-slim

LABEL authors="Dennis Bakhuis"
LABEL version="0.0.1"
LABEL description="Simple Python SSH honeypot server that logs login details to a jsonl file."

RUN pip install --no-cache-dir --upgrade pip
COPY requirements.txt /requirements.txt
RUN pip install --no-cache-dir -r /requirements.txt

RUN mkdir /data
COPY ssh_honeypot/ /ssh_honeypot/

ENV HONEYPOT_PORT=2222
ENV HONEYPOT_OUTPUT_FILE=/data/ssh_honeypot.jsonl
ENV HONEYPOT_MAX_CONNECTIONS=10

WORKDIR /ssh_honeypot
CMD ["python", "main.py"]
