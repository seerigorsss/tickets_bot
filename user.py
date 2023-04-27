from place import Place


class User:
    def __init__(self, telegram_id, score=0, places=set(), city=None):
        self.score = score
        self.places = places
        self.telegram_id = telegram_id
        self.city = city
    
    def get_len_places(self):
        return len(self.places)

    def add_place(self, place: Place):
        self.places.add(place)
        self.score += place.get_score()

    def set_city(self, city):
        self.city = city
    
    def has_city(self) -> bool:
        return (self.city is not None)
    
    def get_city(self) -> str:
        if self.city is None:
            return "нет"
        return self.city

class UserHandler:
    def __init__(self):
        self.users = []
    
    def create_user(self, telegram_id, score=0, places=set(), city=None) -> User:
        user = User(telegram_id, score, places, city)
        self.add_user(user)
        return user

    def add_user(self, user: User):
        self.users.append(user)
    
    def load_users(self):
        pass # TODO: load users from database

    def get_users(self) -> list:
        return self.users
    
    def is_user(self, id) -> bool:
        for elem in self.users:
            if elem.telegram_id == id:
                return True
        return False
    
    def get_user(self, id) -> User:
        for elem in self.users:
            if elem.telegram_id == id:
                return elem
        return None
