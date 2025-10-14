from src.tools.scraper_tools import myStrptime
from src.tools.scraper_tools import makeSoup, futureDate

def formatDate(dateString):
    dateString = dateString.split(" @")[0]
    dateString += " 2024"
    dateFormat = '%B %d %Y'
    date = myStrptime(dateString, dateFormat).date()
    date = futureDate(date)
    return date.strftime('%Y-%m-%d')

def formatPrice(price):
    price = price.replace('FREE','gratis')
    return price.strip().strip(',')

def getData(event):
    titleLink = event.select_one('a.tribe-events-calendar-list__event-title-link')
    priceElement = event.select_one('.tribe-events-c-small-cta__price')
    eventData = {
        'date': formatDate(event.select_one('.tribe-event-date-start').text),
        'time': event.select_one('.tribe-event-date-start').text.split("@")[1].split('-')[0].strip(),
        'title': titleLink.text.strip(),
        'venue': event.select_one('.tribe-events-calendar-list__event-venue-title').text.strip(),
        'price': formatPrice(priceElement.text) if priceElement else "",
        'site': titleLink.get('href'),
        'address': event.select_one('.tribe-events-calendar-list__event-venue-address').text.strip()
    }
    return eventData

def getEventList():
    url = 'https://kompaanbier.nl/nl/eventsurlslug/lijst/'
    events = makeSoup(url).select('.tribe-events-calendar-list__event-row')
    return events

def bot():
    return map(getData, getEventList())
