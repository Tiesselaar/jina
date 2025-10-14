from src.tools.scraper_tools import myStrptime
from src.tools.scraper_tools import makeSoup, futureDate

CALENDARS = ['theaterAmsterdam', 'jazzAmsterdam', 'classicalAmsterdam']

def formatDate(dateString):
    dateFormat = '%A %d %B %Y'
    date = myStrptime(dateString, dateFormat).date()
    return date.strftime('%Y-%m-%d')

def getData(event):
    event_data =  {
        'date': formatDate(event.select_one('.event_date').text.strip()),
        'time': event.select_one('.event_time').text.strip(),
        'title': event.select_one('h2').text.strip(),
        'venue': "Torpedo Theater",
        'price': event.select_one('.event_price').text.strip().replace(' ','').replace(',','.'),
        'site': 'https://www.torpedotheater.nl/' + event.select_one('a').get('href'),
        'address': "Sint Pieterspoortsteeg 33, 1012 HM Amsterdam"
    }
    description = event.text.lower()
    yield {**event_data, 'calendar': 'theaterAmsterdam'}
    if "jazz" in description:
        yield {**event_data, 'calendar': 'jazzAmsterdam'}
    if ("klassiek" in description and ("music" in description or "muziek" in description) or
        "flamenco" in description):
        yield {**event_data, 'calendar': 'classicalAmsterdam'}


def getEventList():
    url = 'https://www.torpedotheater.nl'
    events = makeSoup(url).select('li.voorstelling')
    return events

def bot():
    return (gig for event in getEventList() for gig in getData(event))
