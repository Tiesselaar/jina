from src.tools.scraper_tools import myStrptime
from src.tools.scraper_tools import makeSoup

def formatDate(dateString):
    dateFormat = '%d %b %Y'
    date = myStrptime(dateString, dateFormat)
    return date.strftime('%Y-%m-%d')

def getData(event):
    return {
        'date': formatDate(event.select_one('time.events-event-text-date').contents[0].strip()),
        'time': event.select_one('time.events-event-text-date').contents[2].split('-')[0].strip(),
        'title': event.select_one('h4 span').text,
        'venue': "Framer Framed",
        'price': "",
        'site': event.get('href'),
        'address': "Oranje-Vrijstaatkade 71, 1093 KS Amsterdam"
    }

def getEventList():
    url = 'https://framerframed.nl/agenda'
    return makeSoup(url).select('.events-title:-soup-contains("Agenda")+div a')

def bot():
    return map(getData, getEventList())