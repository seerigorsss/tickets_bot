class Weather:
    # BY TEMPERATURE
    TEMPERATURE_VERY_COLD = 0 # <= -20 C
    TEMPERATURE_COLD = 1 # <= 0 C
    TEMPERATURE_NORMAL = 2 # <= 10 C
    TEMPERATURE_WARM = 3 # <= 20 C
    TEMPERATURE_VERY_WARM = 4 # > 20 C

    # BY WEATHER
    WEATHER_SUN = 5
    WEATHER_RAIN = 6
    WEATHER_SNOW = 7
    WEATHER_THUNDER = 8

class WeatherHandler:
    def __init__(self):
        pass # TODO: initialize YandexWeatherAPI to provide answers
    
    def get_weather(self, place: str):
        return (Weather.TEMPERATURE_VERY_COLD, Weather.WEATHER_RAIN)
