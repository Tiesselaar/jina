from src.tools.scraper_tools import myStrptime
from src.tools.scraper_tools import makeSoup

CALENDARS = ['booksAmsterdam', 'alternativeAmsterdam']

def formatDate(dateString):
    dateFormat = '%d %B %Y'
    date = myStrptime(dateString, dateFormat).date()
    return date.strftime('%Y-%m-%d')

def getData(event):
    eventData = {
        'date': formatDate(event.select_one('.fvsj-list-event-info .fvsj-list-event-date-highlight').text),
        'time': event.select_one('.fvsj-list-event-open').text.split('-')[0].split()[1].strip(),
        'title': event.select_one('.fvsj-list-event-info .fvsj-list-event-link a').text,
        'venue': "Het Fort van Sjakoo",
        'price': "",
        'site': event.select_one('.fvsj-list-event-info .fvsj-list-event-link a').get('href'),
        'address': "Jodenbreestraat 24, 1011 NK Amsterdam"
    }
    for calendar in CALENDARS:
        yield {**eventData, 'calendar': calendar}

def getEventList():
    url = 'https://sjakoo.nl/evenementen/'
    events = makeSoup(url).select('.em-events-list .fvsj-list-event-container')
    return events

def bot():
    return (gig for event in getEventList() for gig in getData(event))
