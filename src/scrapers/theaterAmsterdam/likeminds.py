from src.tools.scraper_tools import myStrptime
from src.tools.scraper_tools import makeSoup
import requests

def getData(event):
    location = event.select_one('.agenda-locatie').text.strip()
    if (
            "Likeminds" in location or
            "Amsterdam Noord" in location
        ):
        venue = "Likeminds"
        address = "Gedempt Hamerkanaal 203, 1021 KP Amsterdam"
    else:
        raise Exception('Unknown venue: ' + location)
    
    try:
        voordemensen_id = event.select_one('a[href^="https://tickets.voordemensen.nl"]').get('href').split('/')[-1]
    except Exception as e:
        if "echo van asterdorp".lower() in event.select_one('.agenda-title').text:
            print('echo van asterdorp event, skipping...')
            return
        if "fringe" in event.select_one('.agenda-custom-type').text.lower():
            print('Fringe event, skipping...')
            return
        raise Exception('No Voordemensen ID found for event: ' + event.select_one('.agenda-title').text.strip()) from e
    
    try:
        subevents = requests.get('https://api.voordemensen.nl/v1/likeminds/events/' + voordemensen_id).json()[0]['sub_events']
    except Exception as e:
        if "Sofie Kramer" in event.select_one('.agenda-title').text:
            print('Sofie Kramer event, skipping...')
            return
        raise Exception('No subevents found for event: ' + event.select_one('.agenda-title').text.strip()) from e

    for subevent in subevents:
        yield {
            'date': subevent['event_date'],
            'time': subevent['event_time'][:5],
            'title': event.select_one('.agenda-title').text.strip(),
            'venue': venue,
            'price': '€' + requests.get('https://api.voordemensen.nl/v1/likeminds/tickettypes/' + str(subevent['event_id'])).json()[0]['base_price'],
            'site': event.select_one('.lees-meer-link').get('href'),
            'address': address
        }
        
def getEventList():
    url = 'https://likeminds.nl/agendatype/noord/'
    events = makeSoup(url).select('.agenda .agenda-row')
    return events

def bot():
    return (gig for event in getEventList() for gig in getData(event))
