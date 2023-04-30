import requests
from aiogram.utils import markdown
from config_reader import config

API_KEY = "b7acf9ac-111a-4d6e-bb9f-d2ce0ecd766d"
STATIONS = dict()
TRANSPORT = dict()

def load_data():
    global STATIONS
    global TRANSPORT
    STATIONS["МОСКВА"] = "c213"
    STATIONS["САНКТ-ПЕТЕРБУРГ"] = "c2"

    TRANSPORT["САМОЛЕТ"] = "plane"
    TRANSPORT["ПОЕЗД"] = "train"
    TRANSPORT["ЭЛЕКТРИЧКА"] = "suburban"
    TRANSPORT["АВТОБУС"] = "bus"

def get_schedule(city1, city2, date, transport):
    response = requests.get(f"https://api.rasp.yandex.net/v3.0/search/?apikey={API_KEY}&" \
                            f"format=json&" \
                            f"from={STATIONS[city1.upper()]}&" \
                            f"to={STATIONS[city2.upper()]}&" \
                            f"lang=ru_RU&" \
                            f"limit=10&" \
                            f"transport_types={TRANSPORT[transport.upper()]}&" \
                            f"date={date}").json()
    answer = [f"Ближайшие 10 рейсов из {city1} в {city2} на указанную дату:"]
    for segment in response["segments"]:
        thread = segment["thread"]
        ticket_info = segment["tickets_info"]
        short_title = thread["short_title"]
        title = thread["title"]
        has_tickets = len(ticket_info["places"]) > 0
        lowest_price = -1
        currency = "RUB"
        if has_tickets:
            for ticket in ticket_info["places"]:
                current_price = ticket["price"]["whole"]
                if lowest_price == -1 or current_price < lowest_price:
                    lowest_price = current_price
                    currency = ticket["currency"]
            ticket_str = f"Билеты от {lowest_price} {currency}"
        else:
            ticket_str = "Нет информации о билетах"
        number = thread["number"]
        url = thread["carrier"]["url"]
        if number == "":
            number = short_title
            if short_title == "":
                number = title
        
        if url == "":
            text = f"Рейс {number}. {ticket_str}"
        else:
            text = markdown.hlink(f"Рейс {number}. ", url) + ticket_str
        answer.append(text)
    if len(answer) == 1:
        answer.append("нет")
    answer = "\n".join(answer)
    return answer
