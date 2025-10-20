from src.tools.scraper_tools import myStrptime
from src.tools.scraper_tools import makeSeleniumSoup, futureDate

CALENDARS = ['danceAmsterdam', 'theaterAmsterdam']

def formatLocation(locationString):
    if "Bau, Van Diemenstraat 408-410" in locationString:
        return "Bau", "Van Diemenstraat 408-410"
    if "Bau, Entrepotdok 4 Amsterdam" in locationString:
        return "Bau", "Entrepotdok 4, 1018 AD Amsterdam"
    raise Exception("Unknown location: " + locationString)

def getData(event):
    venue, address = formatLocation(event.select_one('p.entry-calendar-event-item-text-location').text)
    eventData = {
        'date': event.select_one('.entry-calendar-event-item-text-datetime time').get('datetime'),
        'time': event.select('.entry-calendar-event-item-text-datetime time')[1].get('datetime'),
        'title': event.select_one('h3.entry-calendar-event-item-text-project').text,
            # " - " + \
            # event.select_one('h3.entry-calendar-event-item-text-title').text,
        'venue': venue,
        'price': "",
        'site': event.select_one('a.flag-target').get('href'),
        'address': address
    }
    yield {**eventData, 'calendar': 'danceAmsterdam'}
    yield {**eventData, 'calendar': 'theaterAmsterdam'}

def getEventList():
    url = 'https://bau.amsterdam'
    events = makeSeleniumSoup(url).select('.section-content-home .content-part .entry-calendar .entry-calendar-event.is-shown')
    return events

def bot():
    return (gig for event in getEventList() for gig in getData(event))