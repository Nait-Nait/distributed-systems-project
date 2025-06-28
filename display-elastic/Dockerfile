FROM python:3.10-slim

WORKDIR /app

COPY load_to_elasticsearch.py .

RUN pip install requests

CMD ["python", "load_to_elasticsearch.py"]
