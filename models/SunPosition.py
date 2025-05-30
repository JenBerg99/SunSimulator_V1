from pydantic import BaseModel, Field

class SunPosition(BaseModel):
    # Elevation of the sun in degrees. Range: -90 (below horizon) to 90 (zenith).
    elevation: float = Field(..., ge=-90.0, le=90.0, description="Elevation in degrees (-90 to 90)")

    # Azimuth angle of the sun in degrees. Range: 0 to 360.
    azimuth: float = Field(..., ge=0.0, le=360.0, description="Azimuth in degrees (0 to 360)")
