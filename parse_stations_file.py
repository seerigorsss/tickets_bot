import json


data = json.load(open("stations.json", "r"))

# Example: Select the first item in the list
answering_dict = dict()

for country in data["countries"]:
    print(f"Обработка {country['title']}...")
    cities = 0
    for regions in country["regions"]:
        print(f"Обработка региона {regions['title']}")
        for settlement in regions["settlements"]:
            if "yandex_code" in settlement["codes"]:
                answering_dict[(settlement["title"]).upper()] = settlement["codes"]["yandex_code"]
                cities += 1
    print(f"Всего добавлено {cities} населенных пунктов")

with open("answer.json", "w", encoding="UTF-8") as file:
    for key in answering_dict:
        file.write(f"{key}={answering_dict[key]}\n")
