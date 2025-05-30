from pydantic import BaseModel, Field, field_validator
from typing import Tuple

class SunLightProperties(BaseModel):
    # Brightness percentage represented as a float between 0 and 100
    brightness_percent: float = Field(..., ge=0, le=100, description="Brightness percentage (0–100)")

    # Color temperature of sunlight in Kelvin. Must be between 1000 and 10000.
    color_temperature_k: int = Field(..., ge=1000, le=10000, description="Color temperature in Kelvin (1000–10000)")

    # RGB representation of the sunlight color. Each component must be in the 0–255 range.
    rgb_color: Tuple[int, int, int] = Field(..., description="RGB tuple (each 0–255)")

    @field_validator("rgb_color")
    @classmethod
    def validate_rgb_range(cls, value):
        # Ensures all RGB values are within the valid range
        if any(not (0 <= x <= 255) for x in value):
            raise ValueError("Each RGB component must be between 0 and 255.")
        return value