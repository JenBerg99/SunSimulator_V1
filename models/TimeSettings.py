from pydantic import BaseModel, field_validator
from datetime import time

class TimeSettings(BaseModel):
    # Current time of the simulation
    current_time: time

    # Time of sunrise
    sunrise: time

    # Time of sunset
    sunset: time

    @field_validator("sunset")
    @classmethod
    def validate_sunset_after_sunrise(cls, sunset, info):
        # Ensures sunset is after sunrise
        sunrise = info.data.get("sunrise")
        if sunrise and sunset <= sunrise:
            raise ValueError("Sunset must be after sunrise.")
        return sunset
