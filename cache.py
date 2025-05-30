from models import Location, WeatherInfo, TimeSettings, SunPosition, SunLightProperties
from threading import Lock
from datetime import datetime, timedelta
from services import calculate_sun_position, calculate_sunlight_properties
import threading

class GlobalCache:
    def __init__(self):
        self.lock = Lock()
        self.time_settings = TimeSettings(current_time=datetime.now())
        self.location = Location(latitude=0.0, longitude=0.0)
        self.weather_info = WeatherInfo(
            visibility_m=10000,
            rain_mm=0.0,
            cloud_coverage_percent=0.0,
            sunrise=datetime.now().time(),
            sunset=datetime.now().time(),
            humidity_percent=50.0,
            temperature_c=20.0
        )        
        self.sun_position = calculate_sun_position(self.location, self.time_settings)
        self.sunlight_properties = calculate_sunlight_properties(self.sun_position, self.weather_info, self.time_settings.current_time)
        self._start_time_updater()        

    def _start_time_updater(self):
        def update_time():
            while True:
                with self.lock:
                    if not self.time_settings.fixed_time:
                        self.time_settings.current_time += timedelta(minutes=1)
                threading.Event().wait(60)

        thread = threading.Thread(target=update_time, daemon=True)
        thread.start()

    def get_time(self):
        with self.lock:
            return self.time_settings

    def set_time(self, ts: TimeSettings):
        with self.lock:
            self.time_settings = ts

    def get_location(self):
        with self.lock:
            return self.location

    def set_location(self, loc: Location):
        with self.lock:
            self.location = loc

    def get_weather(self):
        with self.lock:
            return self.weather_info

    def set_weather(self, weather: WeatherInfo):
        with self.lock:
            self.weather_info = weather
            
    def get_sun_position(self):
        with self.lock:
            if not self.sun_position.manual_override:
                self.sun_position = calculate_sun_position(self.location, self.time_settings)
            return self.sun_position
        
    def set_sun_position(self, sunpos: SunPosition):
        with self.lock:
            self.sun_position = sunpos
            
    def get_sun_light_properties(self):
        with self.lock:            
            self.sunlight_properties = calculate_sunlight_properties(self.sun_position, self.weather_info, self.time_settings.current_time)   
            return self.sunlight_properties       
        
    def set_sun_light_properties(self, sunlightprops: SunLightProperties):
        with self.lock:
            self.set_sun_light_properties = sunlightprops    


cache = GlobalCache()