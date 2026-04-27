from typing import List

from sensor.sensor_data import TemperatureAlert
from kafka_utils.kafka_producer import get_kafka_producer, send_message
from kafka_utils.kafka_consumer import get_kafka_consumer
from sensor.sensor import Sensor


def run_sensor(sensor_id: str, iterations: int):
    sensor = Sensor(sensor_id)
    with get_kafka_producer() as producer:
        for _ in range(iterations):
            sensor.publish(producer)

def catch_exceptions(sensor_ids: List[str]):
    sensor_id_set = set(sensor_ids)
    with get_kafka_consumer(group_id='sensor_monitor') as consumer, \
         get_kafka_producer() as producer:
        consumer.subscribe(['building_sensors'])
        for message in consumer:
            decoded_message = message.value
            sensor_id = decoded_message['sensor_id']
            print(f"[READ] topic={message.topic} partition={message.partition} offset={message.offset} sensor={sensor_id}")
            if sensor_id in sensor_id_set and decoded_message['temperature'] > 40:
                print(f"[ALERT] sensor={sensor_id} temperature={decoded_message['temperature']:.2f} -> publishing to temperature_alerts")
                send_message(
                    producer,
                    'temperature_alerts',
                    TemperatureAlert(sensor_id=sensor_id, temperature=decoded_message['temperature']).model_dump()
                )

def get_alerts():
    with get_kafka_consumer(group_id='alert_reader') as consumer:
        consumer.subscribe(['alerts'])
        for message in consumer:
            print(f"[READ] topic={message.topic} alert={message.value}")
