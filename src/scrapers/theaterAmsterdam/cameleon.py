from src.tools.scraper_tools import myStrptime
from src.tools.scraper_tools import makeSoup

def formatDate(dateString):
    dateString = " ".join(dateString.split()[:3])
    dateFormat = '%d %B %Y'
    date = myStrptime(dateString, dateFormat)
    return date.strftime('%Y-%m-%d')

def getData(event):
    if "Dit is een TestTitel" in event.text:
        return
    return {
        'date': formatDate(event.select_one('.custom-list-details .custom-list-time').text),
        'time': event.select_one('.custom-list-details .custom-list-time').text.split("-")[0].split()[-1],
        'title': event.select_one('.custom-list-details h3').text,
        'venue': "De Cameleon",
        'price': "",
        'site': event.select_one('a.custom-event-list-item-link').get('href'),
        'address': "Derde Kostverlorenkade 35, 1054 TS Amsterdam"
    }

def getEventList():
    url = 'https://www.decameleon.nl/agenda/'
    events = makeSoup(url).select('.em-events-list .custom-event-list-item-wrapper')
    return events

def bot():
    return map(getData, getEventList())