import requests
import json


def get_events():
    url = "https://www.goethe.de/rest/objeventcalendarRedesign/events/fetchEvents"
    config_data = {
        "institute_ID": 351,
        "elementsperpage": 15,
    }
    params = {
        "configData": json.dumps(config_data),
        "langId": "33",
        "viewMode": "-1",
    }

    response = requests.get(url, params=params)

    print(json.dumps([event for event in response.json()["eventItems"]], indent=2))


if __name__ == "__main__":
    get_events()