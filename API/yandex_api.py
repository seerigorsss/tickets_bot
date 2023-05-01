import requests
from aiogram.utils import markdown

# from config_reader import config

API_KEY = "b7acf9ac-111a-4d6e-bb9f-d2ce0ecd766d"
TICKET_URL = "https://travel.yandex.ru/avia/flights/"
STATIONS = dict()
TRANSPORT = dict()


def load_data():
    global STATIONS
    global TRANSPORT
    with open("station_list", "r", encoding="utf-8") as file:
        for i in range(13355):
            current_line = file.readline().strip("\n").split("=")
            STATIONS[current_line[0]] = (current_line[1], "moskva")

    TRANSPORT["САМОЛЕТ"] = "plane"
    TRANSPORT["ПОЕЗД"] = "train"
    TRANSPORT["ЭЛЕКТРИЧКА"] = "suburban"
    TRANSPORT["АВТОБУС"] = "bus"


def get_url(transport_type, number, city1, city2, date):
    if transport_type == TRANSPORT["САМОЛЕТ"]:
        return f"{TICKET_URL}{number}"
    if transport_type == TRANSPORT["ПОЕЗД"]:
        return f"https://travel.yandex.ru/trains/?when={date}"
    if transport_type == TRANSPORT["ЭЛЕКТРИЧКА"]:
        return f"https://travel.yandex.ru/buses/?when={date}"
    if transport_type == TRANSPORT["АВТОБУС"]:
        return f"https://travel.yandex.ru/trains/?when={date}"


def get_schedule(city1, city2, date, transport, format=False):
    response = requests.get(f"https://api.rasp.yandex.net/v3.0/search/?apikey={API_KEY}&" \
                            f"format=json&" \
                            f"from={STATIONS[city1.upper()][0]}&" \
                            f"to={STATIONS[city2.upper()][0]}&" \
                            f"lang=ru_RU&" \
                            f"limit=10&" \
                            f"transport_types={TRANSPORT[transport.upper()]}&" \
                            f"date={date}").json()
    answer = [f"Ближайшие 10 рейсов из {city1} в {city2} на указанную дату:"]
    trips = []
    print(response)
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
        number = "-".join(thread["number"].split())
        url = get_url(TRANSPORT[transport.upper()], number, city1, city2, date)
        if number == "":
            number = short_title
            if short_title == "":
                number = title

        if url == "":
            text = f"Рейс {number}. {ticket_str}"
        else:
            text = markdown.hlink(f"Рейс {number}. ", url) + ticket_str
        answer.append(text)
        trip = dict()
        trip["source_title"] = segment["from"]["title"]
        trip["target_title"] = segment["to"]["title"]
        trip["source_date"] = segment["arrival"]
        trip["target_date"] = segment["departure"]
        trip["price"] = lowest_price if has_tickets else 0
        trip["name"] = f"Рейс {number}"
        trips.append(trip)
    if len(answer) == 1:
        answer.append("нет")
    answer = "\n".join(answer)

    return (answer, trips)
