from models.WeatherInfo import WeatherInfo
from models.TimeSettings import TimeSettings
from models.SunPosition import SunPosition
from models.SunLightProperties import SunLightProperties
from models.CompleteModel import CompleteModel
from threading import Lock
from datetime import datetime, timedelta, time

class GlobalCache:
    def __init__(self):
        self.lock = Lock()
        self.time_settings = TimeSettings(
            current_time=datetime.now().time(),
            sunrise=time(8, 0, 0),
            sunset=time(18, 0, 0)
        )        
        self.sun_position = SunPosition(
            elevation=90.0,
            azimuth= 180
        )
        self.weather_info = WeatherInfo(
            visibility=10000,
            rain_mm=0.0,
            cloud_coverage_percent=0.0
        )                
        self.sunlight_properties = SunLightProperties(
            brightness_percent=5,
            color_temperature_k=2000,
            rgb_color=[255,255,255]
        )           
        self.complete_model = CompleteModel(                
            timesettings=self.time_settings,
            sunposition=self.sun_position,
            weatherinfo=self.weather_info,
            sunlightproperties=self.sunlight_properties
        )
        self._observers = []

    def register_observer(self, callback):
        """Register Callback Function"""
        self._observers.append(callback)    

    def _notify_observer(self):
        """Notify all Observer"""
        for callback in self._observers:
            callback(self.sunlight_properties)
    
    def get_time(self):
        with self.lock:
            return self.time_settings

    def set_time(self, ts: TimeSettings):
        with self.lock:
            self.time_settings = ts

    def get_sun_position(self):
        with self.lock:
            return self.sun_position

    def set_sun_position(self, sunposition: SunPosition):
        with self.lock:
            self.sun_position = sunposition
            
    def get_weather(self):
        with self.lock:
            return self.weather_info

    def set_weather(self, weather: WeatherInfo):
        with self.lock:
            self.weather_info = weather
            
    def get_sunlight_properties(self):
        with self.lock:
            return self.sunlight_properties

    def set_sunlight_properties(self, sunlight: SunLightProperties):        
        with self.lock:
            self.sunlight_properties = sunlight     
        self._notify_observer()       

    def get_complete_model(self):
        with self.lock:
            return self.complete_model
            
    def set_complete_model(self, completemodel: CompleteModel):
        with self.lock:
            self.time_settings = completemodel.timesettings
            self.sun_position = completemodel.sunposition
            self.weather_info = completemodel.weatherinfo
            self.sunlight_properties = completemodel.sunlightproperties
            
            self.complete_model = CompleteModel(                
                timesettings=self.time_settings,
                sunposition=self.sun_position,
                weatherinfo=self.weather_info,
                sunlightproperties=self.sunlight_properties
            )
        self._notify_observer()

cache = GlobalCache()