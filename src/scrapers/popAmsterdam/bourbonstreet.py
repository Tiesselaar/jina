from src.tools.scraper_tools import myStrptime
from src.tools.scraper_tools import makeSoup, futureDate

# CALENDARS = ['theaterAmsterdam', 'classicalAmsterdam']

def formatDate(dateString):
    day, month, year = dateString.split()
    month = month[:3]
    dateString = " ".join([day, month, year])
    dateFormat = '%d %b %Y'
    date = myStrptime(dateString, dateFormat)
    return date.strftime('%Y-%m-%d')


def getData(event):
    return {
        'date': formatDate(event.select_one('[data-hook="date"]').text.split(',')[0]),
        'time': event.select_one('[data-hook="date"]').text.split(',')[1].split()[0],
        'title': event.select_one('span[data-hook="ev-list-item-title"]').text,
        'venue': "Bourbon Street",
        'price': "",
        'site': event.select_one('a[data-anchor="event-details"]').get('href'),
        'address': "Leidsekruisstraat 6-8, 1017 RH Amsterdam"
    }

def getEventList():
    url = 'https://www.bourbonstreet.nl/shows'
    events = makeSoup(url).select('#wix-events-widget li[data-hook="event-list-item"]')
    return events

def bot():
    return map(getData, getEventList())
    # return (gig for event in getEventList() for gig in getData(event))
