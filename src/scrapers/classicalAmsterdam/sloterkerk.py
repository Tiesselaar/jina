from src.tools.scraper_tools import makeSoup

def getData(event):
    if ("Orgeltochten Noord-Holland" in event.text and
        "2 augustus" in event.text):
        time = "10:30"
    else:
        time = None
    return {
        'date': event.select_one('article header time').get('datetime'),
        'time': time or event.select_one('article header time .tribe-event-date-start').text.split()[-1],
        'title': event.select_one('h3.tribe-events-calendar-list__event-title a').text.strip(),
        'venue': event.select_one('address .tribe-events-calendar-list__event-venue-title').text.strip(),
        'price': event.select_one('.tribe-events-c-small-cta__price').text.strip(),
        'site': event.select_one('h3.tribe-events-calendar-list__event-title a').get('href'),
        'address': event.select_one('address .tribe-events-calendar-list__event-venue-address').text.strip()
    }

def getEventList():
    url = 'https://sloterkerk.nl/events/'
    events = makeSoup(url).select('.tribe-events-calendar-list .tribe-events-calendar-list__event-row')
    return events

def bot():
    return map(getData, getEventList())
