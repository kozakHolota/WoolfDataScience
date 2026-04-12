import json
import uuid
from contextlib import contextmanager
from typing import Any, Generator

from kafka import KafkaProducer

from config import kafka_config


@contextmanager
def get_kafka_producer() -> Generator[KafkaProducer, Any, None]:
    """Get a Kafka producer."""
    producer = KafkaProducer(
        **kafka_config,
        value_serializer=lambda v: json.dumps(v).encode('utf-8'),
        key_serializer=lambda v: json.dumps(v).encode('utf-8')
    )
    try:
        yield producer
    finally:
        producer.close()

def send_message(kafka_producer: KafkaProducer, topic: str, value: dict) -> None:
    """Send a message to Kafka topic."""
    key = str(uuid.uuid4())
    try:
        kafka_producer.send(topic, value=value, key=key)
        kafka_producer.flush()
        print(f"[SENT] topic={topic} key={key} value={value}")
    except Exception as e:
        raise e