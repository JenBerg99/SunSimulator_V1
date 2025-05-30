from pydantic import BaseModel, Field

class WeatherInfo(BaseModel):
    # Visibility in meters. Must be between 0 and 50,000.
    visibility: float = Field(..., ge=0, le=50000, description="Visibility in meters (0–50000 m)")

    # Rainfall amount in millimeters. Must be between 0 and 1,000.
    rain_mm: float = Field(..., ge=0, le=1000, description="Rainfall in millimeters (0–1000 mm)")

    # Cloud coverage as a float between 0.0 (clear) and 100 (fully overcast).
    cloud_coverage_percent: float = Field(..., ge=0.0, le=100, description="Cloud coverage (0 = clear, 100 = fully covered)")
