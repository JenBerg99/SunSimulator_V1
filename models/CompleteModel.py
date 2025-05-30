from pydantic import BaseModel
from models.WeatherInfo import WeatherInfo
from models.TimeSettings import TimeSettings
from models.SunPosition import SunPosition
from models.SunLightProperties import SunLightProperties

class CompleteModel(BaseModel):
    # Contains weather-related inputs like cloud coverage and rain.
    weatherinfo: WeatherInfo
    
    # Time-related information such as current time and daylight bounds.
    timesettings: TimeSettings

    # Position of the sun (azimuth and elevation).
    sunposition: SunPosition

    # Calculated sunlight properties based on other inputs.
    sunlightproperties: SunLightProperties

class CompleteModelSmall(BaseModel):
    # Contains weather-related inputs like cloud coverage and rain.
    weatherinfo: WeatherInfo
    
    # Time-related information such as current time and daylight bounds.
    timesettings: TimeSettings

    # Position of the sun (azimuth and elevation).
    sunposition: SunPosition
