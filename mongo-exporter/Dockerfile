FROM python:3.11-slim

WORKDIR /app
COPY export.py .
RUN pip install pymongo

CMD ["python", "export.py"]
