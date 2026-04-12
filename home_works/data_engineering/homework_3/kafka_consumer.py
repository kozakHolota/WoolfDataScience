import json
from contextlib import contextmanager
from typing import Any, Generator

from kafka import KafkaConsumer

from config import kafka_config


@contextmanager
def get_kafka_consumer() -> Generator[KafkaConsumer, Any, None]:
    """Get a Kafka consumer."""
    kafka_consumer = KafkaConsumer(
        **kafka_config,
        value_deserializer=lambda v: json.loads(v.decode('utf-8')),
        key_deserializer=lambda v: json.loads(v.decode('utf-8')),
        auto_offset_reset='earliest',  # Зчитування повідомлень з початку
        enable_auto_commit=True,  # Автоматичне підтвердження зчитаних повідомлень
        group_id='my_consumer_group_3',  # Ідентифікатор групи споживачів
        consumer_timeout_ms=5000,  # Вийти з for-loop після 5с без нових повідомлень
    )
    try:
        yield kafka_consumer
    finally:
        kafka_consumer.close()

@contextmanager
def consume_kafka_messages(kafka_consumer: KafkaConsumer, topic_name: str) -> Generator[dict, Any, None]:
    """Consume Kafka messages."""
    kafka_consumer.subscribe([topic_name])
    try:
        for message in kafka_consumer:
            print(f"[READ] topic={topic_name} partition={message.partition} offset={message.offset} value={message.value}")
            yield message.value
    except Exception as e:
        print(f"Error consuming Kafka messages: {e}")
        raise