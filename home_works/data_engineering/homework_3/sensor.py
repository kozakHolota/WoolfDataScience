import random

from sensor_data import SensorData
from kafka_producer import get_kafka_producer, send_message


class Sensor:
    def __init__(self, sensor_id: str):
        self.sensor_id = sensor_id

    def get_temperature(self) -> float:
        return random.uniform(25, 45)

    def get_humidity(self) -> float:
        return random.uniform(15, 85)

    def publish(self):
        with get_kafka_producer() as producer:
            s_data = SensorData(sensor_id=self.sensor_id, temperature=self.get_temperature(), humidity=self.get_humidity())
            print(f"[PUBLISH] sensor={self.sensor_id} topic=building_sensors temperature={s_data.temperature:.2f} humidity={s_data.humidity:.2f}")
            send_message(producer, 'building_sensors', s_data.model_dump())