from src.tools.scraper_tools import makeSoup
from bs4 import BeautifulSoup

CALENDARS = ['popAmsterdam']

def bs(string):
    return BeautifulSoup(string, 'lxml')

def getData(event):
    eventData = {
        'date': event.select_one('header time').get('datetime'),
        'time': event.select_one('header time > .tribe-event-date-start').text.split('@')[1].strip(),
        'title': event.select_one('h3 > a').get('title'),
        'venue': (event.select_one('address .tribe-events-calendar-list__event-venue-title') or bs('Maloe Melo')).text.strip(),
        'price': (event.select_one('.tribe-events-c-small-cta__price') or bs('')).text.strip().lower(),
        'site': event.select_one('h3 > a').get('href'),
        'address': (event.select_one('address .tribe-events-calendar-list__event-venue-address') or
                    bs('Lijnbaansgracht 163, Amsterdam, Noordholland, Nederland')).text.strip()
    }
    yield {**eventData, 'calendar': 'popAmsterdam'}

def getEventList():
    url = 'https://www.maloemelo.com/events/'
    events = makeSoup(url).select('.tribe-events-calendar-list__event-row')
    return events

def bot():
    return (gig for event in getEventList() for gig in getData(event))