from src.tools.scraper_tools import makeSoup

CALENDARS = ['popAmsterdam']

def getData(event):
    eventData = {
        'date': event.select_one('header time').get('datetime'),
        'time': event.select_one('header time > .tribe-event-date-start').text.split('@')[1].strip(),
        'title': event.select_one('h4 > a').get('title'),
        'venue': event.select_one('address .tribe-events-calendar-list__event-venue-title').text.strip(),
        'price': event.select_one('.tribe-events-c-small-cta__price').text.strip().lower(),
        'site': event.select_one('h4 > a').get('href'),
        'address': event.select_one('address .tribe-events-calendar-list__event-venue-address').text.strip()
    }
    yield {**eventData, 'calendar': 'popAmsterdam'}

def getEventList():
    url = 'https://helicopteramsterdam.nl/events/'
    events = makeSoup(url).select('.tribe-events-calendar-list__event-row')
    return events

def bot():
    return (gig for event in getEventList() for gig in getData(event))