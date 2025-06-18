from cache import cache
from models.SunLightProperties import SunLightProperties
from models.CompleteModel import CompleteModel, CompleteModelSmall
from typing import Tuple
import math

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

def calculate_sunlight_properties(complete_model: CompleteModelSmall) -> CompleteModel:
    """
    Calculates sunlight properties such as brightness and color temperature
    based on sun elevation and weather conditions, and updates the given model.
    """

    # Extract sun elevation and cloud coverage from the input model
    elevation = complete_model.sunposition.elevation
    cloud_coverage = max(0, min(complete_model.weatherinfo.cloud_coverage_percent, 100))  # Clamp to [0, 100]

    # Case: Sun is below the horizon → no direct sunlight
    if elevation <= 0:
        # Assumption: No sunlight when sun is below the horizon, so brightness = 0
        # Color temperature is set to 2000K as a placeholder, but in reality, there's no sunlight
        # RGB color is set to black to represent total absence of light
        sunlight = SunLightProperties(
            brightness_percent=0.0,
            color_temperature_k=2000,
            rgb_color=(0, 0, 0)
        )

    else:
        # Base intensity is derived from sun elevation using a sine function:
        # This is a simple physical approximation: sunlight intensity ∝ sin(elevation)
        base_intensity = math.sin(math.radians(elevation)) * 100

        # Cloud attenuation factor:
        # Originally we used a linear formula: (1 - cloud_coverage / 100)
        # However, in practice, even fully overcast skies (100% clouds) let through too much light with that model.
        #
        # Therefore, we now use a quadratic attenuation:
        #     cloud_factor = (1 - cloud_coverage / 100) ** 2
        #
        # This emphasizes that:
        # - Light decreases gradually with low cloud coverage
        # - But drops off sharply as clouds become denser
        #
        # Rationale:
        # Heavy clouds like storm fronts block most sunlight, and human perception of brightness is nonlinear.
        cloud_factor = (1 - cloud_coverage / 100) ** 2

        # Compute brightness 
        brightness = base_intensity * cloud_factor

        # Apply weather-based boost if conditions are ideal
        ideal_conditions = (cloud_coverage < 20 and
                            complete_model.weatherinfo.rain_mm < 1 and
                            complete_model.weatherinfo.visibility >= 10000
                            )
    
        # Ensure brightness is at least 85% under ideal conditions
        if ideal_conditions:
            brightness = max(brightness, 85.0)

        # Clamp brightness to [0, 100]
        brightness = max(0.0, min(brightness, 100.0))

        # Determine color temperature based on sun elevation:
        # - Low elevation (<10°) → warm light (sunrise/sunset) → 2000K
        # - High elevation (>60°) → cool daylight → 6500K
        # - In between → linear interpolation between 2000K and 6500K
        if elevation < 10:
            color_temp = 2000
        elif elevation > 60:
            color_temp = 6500
        else:
            ratio = (elevation - 10) / (60 - 10)
            color_temp = int(2000 + ratio * (6500 - 2000))

        # Convert the Kelvin color temperature to an RGB representation
        rgb = kelvin_to_rgb(color_temp)

        # Assemble the sunlight properties
        sunlight = SunLightProperties(
            brightness_percent=brightness,
            color_temperature_k=color_temp,
            rgb_color=rgb
        )

    # Create and return the updated model with sunlight properties included
    response = CompleteModel(
        **complete_model.model_dump(),
        sunlightproperties=sunlight
    )

    # cache the updated model globally
    cache.set_complete_model(response)

    return response
