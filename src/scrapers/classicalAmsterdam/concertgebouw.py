import requests
import json

CALENDARS = ['classicalAmsterdam', 'jazzAmsterdam']

def getData(event):
    event_data = {
        'date': event['eventStartDate'].split()[0],
        'time': event['eventStartDate'].split()[1],
        'title': event['title'],
        'venue': "Het Concertgebouw",
        'price': "€" + str(event['price']),
        'site': event['url'],
        'address': "Concertgebouwplein 10, 1071 LN Amsterdam"
    }
    yield {
        **event_data,
        'calendar': 'classicalAmsterdam'
    }
    if 'Jazz' in sum(map(lambda x: list(x.values()), event['production'][0]['genres']),[]):
        yield {
            **event_data,
            'calendar': 'jazzAmsterdam'
        }

def getEventList():
    # venue_name for the output file, url for request
    venue_name = 'concertgebouw'
    urls = ('https://bridge.concertgebouw.nl/feed/v2/nl/events?page=' + str(i) for i in range(1,10))
    events = sum((json.loads(requests.get(url).content)['data'] for url in urls), [])
    return events

def bot():
    return [gig for event in getEventList() for gig in getData(event)]