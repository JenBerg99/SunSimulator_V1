from fastapi import APIRouter
from models import Location, WeatherInfo, TimeSettings, SunPosition, SunLightProperties
from cache import cache

router = APIRouter()

# test
@router.get("/sun")
def get_sun_position():
    return cache.get_sun_position()

@router.post("/sun")
def set_sun_position(sun: SunPosition):
    cache.set_sun_position(sun)
    return {"status": "sun position manually overridden"}

@router.get("/time")
def get_time():
    return cache.get_time()

@router.post("/time")
def set_time(ts: TimeSettings):
    cache.set_time(ts)
    return {"status": "updated"}

@router.get("/location")
def get_location():
    return cache.get_location()

@router.post("/location")
def set_location(loc: Location):
    cache.set_location(loc)
    return {"status": "updated"}

@router.get("/weather")
def get_weather():
    return cache.get_weather()

@router.post("/weather")
def set_weather(weather: WeatherInfo):
    cache.set_weather(weather)
    return {"status": "updated"}

@router.get("/sunlight")
def get_sun_light_properties():
    return cache.get_sun_light_properties()    

# @router.post("/sunlight")
# def set_sun_light_properties(sunlightprops: SunLightProperties):
#     cache.set_sun_light_properties(sunlightprops)
#     return {"status": "sun position manually overridden"}
