from src.tools.scraper_tools import myStrptime
from src.tools.scraper_tools import makeSoup, futureDate
from datetime import datetime

CALENDARS = ['alternativeAmsterdam', 'jazzAmsterdam']

def formatTime(time):
    time = " ".join(time.split()[-2:])
    return datetime.strftime(datetime.strptime(time, '%I:%M %p'), '%H:%M')

def getData(event):
    site = event.select_one('h3 > a').get('href')
    description = makeSoup(site).select_one('#tribe-events-content .tribe-events-single-event-description').text.lower()
    try:
        price = event.select_one('.tribe-events-c-small-cta__price').text.strip().lower()
    except:
        price = ""
    eventData = {
        'date': event.select_one('header time').get('datetime'),
        'time': formatTime(event.select_one('header time > .tribe-event-date-start').text),
        'title': event.select_one('h3 > a').get('title'),
        'venue': "Plantage Dok",
        'price': price,
        'site': site,
        'address': "Plantage Doklaan 8-12, 1018CM Amsterdam"
    }

    if (
        "jazz" in description or
        "improvisation" in description and "music" in description or
        "space is the place" in description
    ):
        yield {**eventData, 'calendar': 'jazzAmsterdam'}
    yield {**eventData, 'calendar': 'alternativeAmsterdam'}

def getEventList():
    url = 'https://plantagedok.nl/events/list/'
    events = makeSoup(url).select('.tribe-events-calendar-list__event-row')
    return events

def bot():
    return (gig for event in getEventList() for gig in getData(event))
