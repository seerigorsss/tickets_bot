from weather import Weather


class Place:
    def __init__(self, score, city, possible_temperatures=(Weather.TEMPERATURE_NORMAL), possible_weathers=(Weather.WEATHER_SUN)):
        self.score = score
        self.city = city
        self.possible_temperatures = possible_temperatures
        self.possible_weathers = possible_weathers
    
    def get_score(self):
        return self.score

class PlaceHandler:
    def __init__(self):
        self.places = []
    
    def add_place(self, place: Place):
        self.places.append(place)
    
    def load_places(self):
        pass # TODO: load places from database
    
    def get_places(self, temperature, weather) -> list:
        return_places = []
        for current_place in self.places:
            if (temperature in current_place.possible_temperatures) \
            and (weather in current_place.possible_weathers):
                return_places.append(current_place)
        return current_place
    
    def get_places_limited_by_city(self, city, temperature, weather) -> list:
        return_places = []
        for current_place in self.places:
            if (current_place.city == city) \
            and (temperature in current_place.possible_temperatures) \
            and (weather in current_place.possible_weathers):
                return_places.append(current_place)
        return return_places
