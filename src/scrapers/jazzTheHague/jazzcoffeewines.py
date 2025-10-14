from src.tools.scraper_tools import myStrptime
from src.tools.scraper_tools import makeSoup, futureDate
import re

def formatDate(dateString):
    dateString += " 2024"
    dateFormat = '%a %d %b %Y'
    date = myStrptime(dateString, dateFormat).date()
    date = futureDate(date, 60)
    return date.strftime('%Y-%m-%d')

# def formatTime(time):
#     # format time as '21:00'
#     return time

# def formatPrice(price):
#     # format price as '\u20ac12,50' (no space!)
#     price = price.replace(' ','')
#     return price

def getData(event):
    eventData = {
        'date': formatDate(event[0]),
        'time': event[1].split('-')[0].strip().replace('.',':'),
        'title': event[2].strip(),
        'venue': "Jazz Coffee & Wines",
        'price': "gratis",
        'site': "https://jazzcoffeewines.nl/events/",
        'address': "Noordeinde 90, 2514 GM Den Haag"
    }
    if re.match('^\d\d:\d\d$', eventData['time']):
        return eventData

def getEventList():
    url = 'https://jazzcoffeewines.nl/events/'
    headers = makeSoup(url).select('h2')
    dateFormat = '^[A-Z]{2} \d\d? [A-Z]{3}$'
    events = [[headers[n].text, headers[n+1].text, headers[n+2].text] for n in range(len(headers) - 2) if re.search(dateFormat, headers[n].text)]
    return events

def bot():
    return map(getData, getEventList())
