FROM python:latest

ENV PYTHONUNBUFFERED=1

RUN pip install kafka-python click pydantic

WORKDIR /app

COPY . .

CMD ["python3", "main.py", "--iterations", "20", "--sensors_amount", "5", "--timeout", "20"]
