FROM python:3.8.10-slim

WORKDIR /python_app

RUN pip install --no-cache-dir docker
RUN pip install --no-cache-dir prometheus_client

COPY ./exporter/ /python_app/

CMD python3 exporter.py