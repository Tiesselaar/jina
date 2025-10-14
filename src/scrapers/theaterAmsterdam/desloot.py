from src.tools.scraper_tools import myStrptime
from src.tools.scraper_tools import makeSoup, futureDate

# CALENDARS = ['theaterAmsterdam', 'classicalAmsterdam']

def formatDate(dateString):
    dateString += " 2024"
    dateFormat = '%a %d %B %Y'
    date = myStrptime(dateString, dateFormat).date()
    date = futureDate(date)
    return date.strftime('%Y-%m-%d')

# def formatTime(time):
#     # format time as '21:00'
#     return time

def formatPrice(price):
    if not price:
        return ""
    price = price.text.strip()
    return '€' + price.replace(',','.')

def getData(event):
    site = event.select_one('a').get('href')
    # subsoup = makeSoup(site)
    return {
        'date': formatDate(event.select_one('.events-item__date__start').text.strip()),
        'time': event.select_one('.events-item__date__time').get("content"),
        'title': event.select_one('h2.events-item__title').text.strip(),
        'venue': "De Sloot",
        'price': formatPrice(event.select_one('.events-item__price')),
        'site': site,
        'address': "Rhoneweg 6-10, 1043 AH Amsterdam"
    }

def getEventList():
    url = 'https://desloot.nl/events/'
    events = makeSoup(url).select('.events-list .events-item')
    return events

def bot():
    return map(getData, getEventList())
    # return (gig for event in getEventList() for gig in getData(event))