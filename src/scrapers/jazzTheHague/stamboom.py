from src.tools.scraper_tools import myStrptime
from src.tools.scraper_tools import makeSoup, futureDate


def formatDate(dateString):
    dateString = " ".join(dateString.split()[:4])
    dateFormat = '%d %b %Y %H:%M'
    date = myStrptime(dateString, dateFormat)
    return date.strftime('%Y-%m-%d'), date.strftime('%H:%M')

def getData(event):
    date, time = formatDate(event.select_one('[data-hook="date"]').text)
    eventData = {
        'date': date,
        'time': time,
        'title': event.select_one('[data-hook="ev-list-item-title"]').text,
        'venue': "De Stamboom",
        'price': "gratis",
        'site': event.select_one('a[data-hook="ev-rsvp-button"]').get('href'),
        'address': "Eikstraat 1, 2565 MT Den Haag"
    }
    return eventData

def getEventList():
    url = 'https://www.cafedestamboom.com/evenementen'
    events = makeSoup(url).select('li[data-hook="event-list-item"]')
    return events

def bot():
    return map(getData, getEventList())
