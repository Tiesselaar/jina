from src.tools.scraper_tools import myStrptime
from src.tools.scraper_tools import makeSeleniumSoup, futureDate

CALENDARS = ['classicalAmsterdam', 'theaterAmsterdam']

def formatLocation(locationString):
    if "Bau, Van Diemenstraat 408-410" in locationString:
        return "Bau", "Van Diemenstraat 408-410"
    if "Bau, Entrepotdok 4 Amsterdam" in locationString:
        return "Bau", "Entrepotdok 4, 1018 AD Amsterdam"
    if "Korzo, The Hague" in locationString or \
        "TALA, Zagreb" in locationString:
        return None, None
    if locationString == "Museum Tot Zover":
        return "Museum Tot Zover", "Kruislaan 124, 1097 GA Amsterdam"
    if locationString == "Frascati Amsterdam":
        return "Frascati", "Nes 63, 1012 KD Amsterdam"
    raise Exception("Unknown location: " + locationString)

def getData(event):
    venue, address = formatLocation(event.select_one('p.entry-calendar-event-item-text-location').text)
    if not venue and not address:
        return
    eventData = {
        'date': event.select('.entry-calendar-event-item-text-datetime time')[0].get('datetime'),
        'time': event.select('.entry-calendar-event-item-text-datetime time')[-1].get('datetime'),
        'title': event.select_one('h3.entry-calendar-event-item-text-project').text,
            # " - " + \
            # event.select_one('h3.entry-calendar-event-item-text-title').text,
        'venue': venue,
        'price': "",
        'site': event.select_one('a.flag-target').get('href'),
        'address': address
    }
    yield {**eventData, 'calendar': 'classicalAmsterdam'}
    yield {**eventData, 'calendar': 'theaterAmsterdam'}

def getEventList():
    url = 'https://bau.amsterdam'
    events = makeSeleniumSoup(url).select('.section-content-home .content-part .entry-calendar .entry-calendar-event.is-shown')
    return events

def bot():
    return (gig for event in getEventList() for gig in getData(event))