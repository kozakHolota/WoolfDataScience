FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1

RUN pip install kafka-python-ng click pydantic

WORKDIR /app

COPY . .

CMD ["python3", "main.py", "--iterations", "20", "--sensors_amount", "5", "--timeout", "20"]
