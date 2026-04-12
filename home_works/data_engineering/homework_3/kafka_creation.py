from kafka import KafkaAdminClient
from kafka.admin import NewTopic

from config import kafka_config, kafka_topics

NUM_PARTITIONS = 2
REPLICATION_FACTOR = 1

def get_kafka_adnin() -> KafkaAdminClient:
    return KafkaAdminClient(**kafka_config)

def create_kafka_topics() -> None:
    kafka_admin = get_kafka_adnin()
    try:
        kafka_admin.create_topics(
            new_topics = [
                NewTopic(name=topic_name, num_partitions=NUM_PARTITIONS, replication_factor=REPLICATION_FACTOR)
                for topic_name in kafka_topics
            ]
        )
        kafka_admin.close()
    except Exception as e:
        print(f"Error creating topics: {e}")
        kafka_admin.close()
        raise e
