import datetime
from src.tools.scraper_tools import makeSoup, futureDate

CALENDARS = ["jazzAmsterdam", "alternativeAmsterdam"]


def formatDate(dayMonth):
    day, month = map(int, dayMonth)
    date = futureDate(datetime.date(2024, month, day))
    return date.strftime('%Y-%m-%d')

def getData(event):
    try:
        prijs = event.select_one('.prijs').text.replace('€ ','€').strip()
    except:
        prijs = ""
    eventData = {
        'date': formatDate(event.select_one('.datummaand').strings),
        'time': event.select_one('.tijd').text,
        'title': event.select_one('.titel').text,
        'venue': "Zaal 100",
        'price': prijs,
        'site': event.select_one('a').get('href'),
        'address': 'De Wittenstraat 100, 1052 BA Amsterdam'
    }
    for calendar in CALENDARS:
        yield {**eventData, 'calendar': calendar}

def getEventList():
    url='https://zaal100.nl/'
    events = makeSoup(url).select('.agenda-container .agenda-item')
    return events

def bot():
    return (gig for event in getEventList() for gig in getData(event))