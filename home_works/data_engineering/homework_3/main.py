import uuid
from threading import Thread
from typing import List

import click
from operational import run_sensor, catch_exceptions, get_alerts

def get_sensor_ids(sensors_amount: int) -> List[str]:
    return [f"sensor_{uuid.uuid4()}" for _ in range(sensors_amount)]

def run_sensors(iterations: int, sensor_ids: List[str]) -> List[Thread]:
    return [Thread(target=run_sensor, args=(sensor_id, iterations, )) for sensor_id in sensor_ids]

@click.command()
@click.option('--iterations', default=100, help='Number of iterations')
@click.option('--sensors_amount', default=10, help='Number of sensors')
@click.option('--timeout', default=10, help='Timeout for catching exceptions')
def main(iterations: int, sensors_amount: int, timeout: int):
    sensor_ids = get_sensor_ids(sensors_amount)
    sensors = run_sensors(iterations, sensor_ids)
    for sensor in sensors:
        sensor.start()

    catch_exch = Thread(target=catch_exceptions, args=(sensor_ids, timeout, ))
    catch_exch.start()

    alerts_cacth = Thread(target=get_alerts)
    alerts_cacth.start()

    for sensor in sensors:
        sensor.join()

    catch_exch.join()
    alerts_cacth.join()


if __name__ == "__main__":
    main()