import json
from contextlib import contextmanager
from typing import Any, Generator

from kafka import KafkaConsumer

from kafka_utils.config import kafka_config


@contextmanager
def get_kafka_consumer(group_id: str) -> Generator[KafkaConsumer, Any, None]:
    """Get a Kafka consumer."""
    kafka_consumer = KafkaConsumer(
        **kafka_config,
        value_deserializer=lambda v: json.loads(v.decode('utf-8')),
        key_deserializer=lambda v: json.loads(v.decode('utf-8')),
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        group_id=group_id,
        consumer_timeout_ms=5000,
    )
    try:
        yield kafka_consumer
    finally:
        kafka_consumer.close()