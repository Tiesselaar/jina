import requests
import json

CALENDARS = ['alternativeAmsterdam']

def getData(event):
    if event['event_status'] == "cancelled":
        cancelled = "Cancelled: "
    elif event['event_status'] == "confirmed":
        cancelled = ""
    else:
        return
    address = event['offline'][-1]['address']

    yield {
        'date': event['date_time'][0]['time_start'][:10],
        'time': event['date_time'][0]['time_start'][11:16],
        'title': cancelled + event['title'],
        'venue': address['name_line'] or address['thoroughfare'] or "Amsterdam",
        'price': "",
        'site': event['url'],
        'address': address['thoroughfare'] + ", " + address['locality'],
        'calendar': 'alternativeAmsterdam'
    }


def getEventList():
    url = 'https://radar.squat.net/api/1.2/search/events.json?'
    query = 'facets[city][]=Amsterdam&fields=title,date_time,price,event_status,offline:address,url&limit=600&language=en'
    return json.loads(requests.get(url + query).content)['result'].values()

def bot():
    return [gig for event in getEventList() for gig in getData(event)]