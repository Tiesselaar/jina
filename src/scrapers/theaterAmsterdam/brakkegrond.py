from src.tools.scraper_tools import makeSoup
import requests

# CALENDARS = ['theaterAmsterdam', 'classicalAmsterdam']

def formatPrice(price):
    price = price.replace('.00','')
    return '€' + price

def get_subevent_data(event_id, depth = 0):
    if depth > 1:
        raise Exception('nested subevents')
    event_data = requests.get('https://api.voordemensen.nl/v1/debrakkegrond/events/' + event_id).json()[0]
    if event_data.get('sub_events'):
        for sub_event in event_data['sub_events']:
            unpacked_sub_event_data, = get_subevent_data(str(sub_event['event_id']), depth + 1)
            yield unpacked_sub_event_data
    else:
        tickets = requests.get('https://api.voordemensen.nl/v1/debrakkegrond/tickettypes/' + event_id).json()
        try:
            if tickets['message'] == "sub_event not found":
                return
        except:
            pass
        yield {
            'date': event_data['event_date'],
            'time': event_data['event_time'][:5],
            'price': formatPrice(tickets[0]['base_price'])
        }

def getData(event):
    site = event.select_one('a.card-default').get('href')
    subsoup = makeSoup(site)
    event_details = subsoup.select_one('.event-detail__tickets a.event-detail__tickets-button')
    if event_details == None:
        return
    shop_link = event_details.get('href')
    if (shop_link == None):
        return
    tickets_link = makeSoup(shop_link).select_one('iframe.js-tickets-iframe').get('src')
    event_id = tickets_link.split("?")[0].split('/')[-1]
    for subevent in get_subevent_data(event_id):
        yield {
            **subevent,
            'title': event.select_one('h3.card-default__title').text.strip(),
            'venue': "Brakke Grond",
            'site': site,
            'address': "Nes 45, 1012 KD Amsterdam"
        }


def getEventList():
    url = 'https://brakkegrond.nl/agenda'
    events = makeSoup(url).select('.event-overview__container .event-overview__tab-target:not(.hidden-tab) .card-default__wrap')
    if len(events) < 5:
        raise Exception('Fewer events than Expected')
    return events

def bot():
    return (gig for event in getEventList() for gig in getData(event))
