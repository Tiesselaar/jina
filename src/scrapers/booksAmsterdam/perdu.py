from src.tools.scraper_tools import myStrptime
from src.tools.scraper_tools import makeSoup, futureDate
import requests

CALENDARS = ['theaterAmsterdam', 'booksAmsterdam']

def formatDate(dateString):
    dateString = " ".join(dateString.split()[:2])
    dateString += " 2024"
    dateFormat = '%d %b %Y'
    date = myStrptime(dateString, dateFormat).date()
    date = futureDate(date)
    return date.strftime('%Y-%m-%d')

def getData(event):
    meta_data = event.select_one('.event__meta').text
    if "tickets: gratis" in meta_data.lower():
        price = "free"
    else:
        ticket_button = event.select_one('.buttons a.button[href^="https://tickets.voordemensen.nl"]')
        if ticket_button:
            voordemensen_id = ticket_button.get('href').split('/')[-1]
            sub_events = requests.get("https://api.voordemensen.nl/v1/perdu/events/" + voordemensen_id).json()[0]['sub_events']
            not_livestream, = [sub_event for sub_event in sub_events if 'livestream' not in sub_event['event_name'].lower()]
            tickets = requests.get("https://api.voordemensen.nl/v1/perdu/tickettypes/" + str(not_livestream['event_id'])).json()
            price = '€' + tickets[0]['base_price'].replace('.00', '')
            if price == '€0':
                price = 'free'
        else:
            price = ""
    eventData = {
        'date': formatDate(meta_data.split('|')[0].strip()),
        'time': meta_data.split('|')[0].split()[-1],
        'title': event.select_one('h3.event__title').text,
        'venue': "Perdu",
        'price': price,
        'site': event.select_one('.buttons a.button[href^="https://perdu.nl/agenda/"]').get('href'),
        'address': "Kloveniersburgwal 86, 1012 CZ Amsterdam",
    }
    yield { **eventData, 'calendar': "booksAmsterdam" }
    yield { **eventData, 'calendar': "theaterAmsterdam" }

def getEventList():
    url = 'https://perdu.nl/agenda/'
    events = makeSoup(url).select('.events .event')
    return events

def bot():
    return (gig for event in getEventList() for gig in getData(event))
