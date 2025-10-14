from src.tools.scraper_tools import makeSoup

CALENDARS = ['alternativeAmsterdam', 'jazzAmsterdam']

def getData(event):
    site = event.select_one('h3.tribe-events-calendar-list__event-title a').get('href')
    subsoup = makeSoup(site)
    try:
        time = subsoup.select_one('h2 > .tribe-event-date-start').text.split("|")[1]
    except:
        time = subsoup.select_one('h2 > span.tribe-events-schedule__time--start').text.strip()

    eventData = {
        'date': event.select_one('time.tribe-events-calendar-list__event-date-tag-datetime').get('datetime'),
        'time': time,
        'title': event.select_one('h3.tribe-events-calendar-list__event-title').text.strip(),
        # 'venue': event.select_one('address span.tribe-events-calendar-list__event-venue-title').text.strip(),
        'venue': 'De Tanker in Noord',
        'price': "",
        'site': site,
        # 'address': event.select_one('address span.tribe-events-calendar-list__event-venue-address').text.strip()
        'address': 'Nieuwe Leeuwarderweg 15, 1022BN Amsterdam'
    }
    yield {**eventData, 'calendar': 'alternativeAmsterdam'}
    yield {**eventData, 'calendar': 'jazzAmsterdam'}

def getEventList():
    url = 'https://detanker.nl/cultuurvitrine-locatie/lijst/'
    events = makeSoup(url).select('.tribe-events-calendar-list .tribe-events-calendar-list__event-row')
    return events

def bot():
    return (gig for event in getEventList() for gig in getData(event))