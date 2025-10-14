from src.tools.scraper_tools import myStrptime
from src.tools.scraper_tools import makeSoup, futureDate


def formatDate(dateString):
    dateString += " 2024"
    dateFormat = '%A %d %B %Y'
    date = myStrptime(dateString, dateFormat).date()
    date = futureDate(date, 30)
    return date.strftime('%Y-%m-%d')

def formatPrice(price):
    price = price.replace('FREE','gratis')
    return price.lower()

def getData(event):
    return {
        'date': formatDate(event.select_one('.gmdh-date').text),
        'time': event.select_one('.gmdh-start_time').text[:5],
        'title': event.select_one('.gmdh-title').text.title(),
        'venue': "Café September",
        'price': formatPrice(event.select_one('.gmdh-price').text),
        'site': "https://www.september.nl/agenda/" + event.get('href'),
        'address': "Grote Markt 26, 2511 BG Den Haag"
    }

def getEventList():
    url = 'https://www.september.nl/agenda/'
    events = makeSoup(url).select('#gmdhAgenda > a')
    return events

def bot():
    return map(getData, getEventList())
