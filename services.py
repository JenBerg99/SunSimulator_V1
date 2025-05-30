from astral.location import LocationInfo
from astral.sun import elevation, azimuth
from models import Location, TimeSettings, SunPosition, WeatherInfo, SunLightProperties
from typing import Tuple
import math
import datetime

def calculate_sun_position(cacheLocation: Location, cacheTimeSettings: TimeSettings) -> SunPosition:
    city = LocationInfo(latitude=cacheLocation.latitude, longitude=cacheLocation.longitude)

    altitude = elevation(observer=city.observer, dateandtime=cacheTimeSettings.current_time)
    az = azimuth(observer=city.observer, dateandtime=cacheTimeSettings.current_time)

    return SunPosition(
        altitude=altitude,
        azimuth=az,
        manual_override=False
    )

def kelvin_to_rgb(temp_k: int) -> Tuple[int, int, int]:
    temp = temp_k / 100

    if temp <= 66:
        red = 255
        green = min(max(99.4708 * math.log(temp) - 161.1196, 0), 255)
        blue = 0 if temp <= 19 else min(max(138.5177 * math.log(temp - 10) - 305.0448, 0), 255)
    else:
        red = min(max(329.6987 * ((temp - 60) ** -0.1332047592), 0), 255)
        green = min(max(288.1222 * ((temp - 60) ** -0.0755148492), 0), 255)
        blue = 255

    return int(red), int(green), int(blue)

def calculate_sunlight_properties(
    sun_position: SunPosition,
    weather: WeatherInfo,
    current_time: datetime
) -> SunLightProperties:
    # Keine Sonne sichtbar
    if sun_position.altitude <= 0:
        return SunLightProperties(
            brightness_percent=0.0,
            color_temperature_k=2000,
            rgb_color=(0, 0, 0)
        )

    # Intensität basierend auf Sonnenhöhe
    base_intensity = math.sin(math.radians(sun_position.altitude)) * 100
    cloud_factor = 1 - weather.cloud_coverage_percent / 100
    brightness = max(0, min(base_intensity * cloud_factor, 100))

    # Farbtemperatur basierend auf Höhe
    if sun_position.altitude < 10:
        color_temp = 2000
    elif sun_position.altitude > 60:
        color_temp = 6500
    else:
        # Linear interpolieren zwischen 2000K und 6500K
        ratio = (sun_position.altitude - 10) / (60 - 10)
        color_temp = int(2000 + ratio * (6500 - 2000))

    rgb = kelvin_to_rgb(color_temp)

    return SunLightProperties(
        brightness_percent=brightness,
        color_temperature_k=color_temp,
        rgb_color=rgb
    )