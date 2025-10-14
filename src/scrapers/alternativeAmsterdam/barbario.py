from src.tools.scraper_tools import myStrptime
from src.tools.scraper_tools import makeSoup, futureDate

def formatDate(dateString):
    dateString += " 2024"
    dateFormat = '%d %B %Y'
    date = myStrptime(dateString, dateFormat).date()
    date = futureDate(date, 120)
    return date.strftime('%Y-%m-%d')

def getData(event):
    return {
        'date': formatDate(event.select_one(':scope > p').text.split('-')[0].strip()),
        'time': event.select_one(':scope > p').text.split('-')[-1].strip(),
        'title': event.select_one('h2').text,
        'venue': "Bar Bario",
        'price': "",
        'site': "https://barbario.nl" + event.select_one('a').get('href'),
        'address': "Bilderdijkstraat 186, 1053 LD Amsterdam"
    }

def getEventList():
    url = 'https://barbario.nl/events'
    events = makeSoup(url).select('ul li[class^="styled__CardContainer"]')
    return events[:20]

def bot():
    return map(getData, getEventList())
