from time import sleep
from typing import List

from sensor_data import TemperatureAlert
from kafka_producer import get_kafka_producer, send_message
from kafka_consumer import get_kafka_consumer, consume_kafka_messages
from sensor import Sensor


def run_sensor(sensor_id: str, iterations: int):
    sensor = Sensor(sensor_id)
    for _ in range(iterations):
        sensor.publish()

def catch_exceptions(sensor_ids: List[str], timeout: int):
    for _ in range(timeout):
        with get_kafka_consumer() as consumer:
            consumer.subscribe(['building_sensors'])
            try:
                for message in consumer:
                    with get_kafka_producer() as producer:
                        decoded_message = message.value
                        sensor_id = decoded_message['sensor_id']
                        print(f"[READ] topic={message.topic} partition={message.partition} offset={message.offset} sensor={sensor_id}")
                        if sensor_id in sensor_ids:
                            if decoded_message['temperature'] > 40:
                                print(f"[ALERT] sensor={sensor_id} temperature={decoded_message['temperature']:.2f} -> publishing to temperature_alerts")
                                send_message(
                                    producer,
                                    'temperature_alerts',
                                    TemperatureAlert(sensor_id=sensor_id, temperature=decoded_message['temperature']).model_dump()
                                )
            except Exception as e:
                print(f"Error processing message: {e}")

            sleep(1)

def get_alerts():
    with get_kafka_consumer() as consumer:
        consumer.subscribe(['temperature_alerts', 'humidity_alerts'])
        for message in consumer:
            print(f"[READ] topic={message.topic} alert={message.value}")
