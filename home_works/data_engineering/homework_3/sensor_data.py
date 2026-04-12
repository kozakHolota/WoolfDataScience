from pydantic import BaseModel, Field


class SensorData(BaseModel):
    temperature: float = Field(ge=25, le=45)  # ge=greater or equal, le=less or equal
    humidity: float = Field(ge=15, le=85)
    sensor_id: str

class TemperatureAlert(BaseModel):
    sensor_id: str
    temperature: float

class HumidityAlert(BaseModel):
    sensor_id: str
    humidity: float