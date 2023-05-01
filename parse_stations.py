import json
import requests

# Set the URL of the JSON file
url = "https://api.rasp.yandex.net/v3.0/stations_list/?apikey=b7acf9ac-111a-4d6e-bb9f-d2ce0ecd766d&lang=en_US&format=json"

print("ok")
# Use the requests module to fetch the file
response = requests.get(url)

print(response)

# Save the file to disk
with open("stations.json", "w", encoding="UTF-8") as f:
    json.dump(response.json(), f)

# Select some data from the JSON file
data = json.load(open("stations.json", "r"))

# Example: Select the first item in the list
print(data.recode)
