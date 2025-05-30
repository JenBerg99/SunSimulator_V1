from pydantic import BaseModel
from datetime import datetime, time
from typing import Optional, Tuple

class Location(BaseModel):
    latitude: float
    longitude: float

class WeatherInfo(BaseModel):
    visibility_m: float
    rain_mm: float
    cloud_coverage_percent: float
    sunrise: time
    sunset: time
    humidity_percent: float
    temperature_c: float

class TimeSettings(BaseModel):
    current_time: datetime
    fixed_time: Optional[bool] = False  # false = auto increment
    
class SunPosition(BaseModel):
    altitude: float  # in degrees
    azimuth: float   # in degrees
    manual_override: bool = False # true = manual override
    
class SunLightProperties(BaseModel):
    brightness_percent: float
    color_temperature_k: int
    rgb_color: Tuple[int, int, int]