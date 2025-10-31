import requests
import json
from datetime import datetime

with open('./src/scrapers/clubAmsterdam/raco.graphql', 'r') as file:
    graph_query = file.read()

def payload(id):
    current_time_iso = datetime.today().isoformat() + "Z"
    return {
        "operationName": "GET_EVENTS_LISTING",
        "variables": {
            "indices": ["EVENT"],
            "pageSize": 100,
            "page": 1,
            "aggregations": [],
            "filters": [
                {"type": "CLUB", "value": str(id)},
                {
                    "type": "DATERANGE",
                    "value": json.dumps({"gte": current_time_iso})
                },
            ],
            "sortOrder": "ASCENDING",
            "sortField": "DATE"
        },
        "query": graph_query
    }


def get_events(id):
    url = "https://ra.co/graphql"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36",
        "Content-Type": "application/json",
    }
    return requests.post(url, headers=headers, json=payload(id)).json()['data']['listing']['data']


def get_event_data(venue, event):
    # url_path = event.get("contentUrl")
    # full_url = f"https://ra.co{url_path}" if url_path else None

    return {
        'date': event['startTime'].split('T')[0],
        'time': event['startTime'].split('T')[1][:5],
        'title': event['title'],
        'venue': event['venue']['name'].replace(' Amsterdam', ''),
        'price': "",
        'site': venue['site'],
        'address': event['venue']['address'],
    }


def bot():
    venues = [
        {
            "id": 206210,
            "venue": "Levenslang",
            "site": "https://www.levenslang.amsterdam/programma"
        },
        {
            "id": 232813,
            "venue": "Tillatec",
            "site": "https://www.tillatec.com/events",
        }
    ]
    return  [
        get_event_data(venue, event) for venue in venues for event in get_events(venue['id'])
    ]