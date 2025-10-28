from src.tools.scraper_tools import myStrptime
from src.tools.scraper_tools import makeSoup

def formatDate(dateString):
    dateFormat = '%d.%m.%y'
    date = myStrptime(dateString, dateFormat).date()
    return date.strftime('%Y-%m-%d')

def formatTime(dateString):
    dateFormat = '%A %B %d, %I%p'
    date = myStrptime(dateString, dateFormat)
    return date.strftime('%H:%M')

def getData(event):
    site = event.get('href')
    subsoup = makeSoup(site)
    return {
        'date': formatDate(event.select_one('span').text.strip()),
        'time': formatTime(subsoup.select_one('header.event-header > span').text.strip()),
        'title': event.select_one('h3').text.strip(),
        'venue': "San Serriffe",
        'price': "",
        'site': site,
        'address': "Sint Annenstraat 30, 1012 HE Amsterdam"
    }

def getEventList():
    url = 'https://san-serriffe.com/events/'
    events = makeSoup(url).select('.content .main .event-list .event-list__item')[:10]
    return events

def bot():
    from concurrent.futures import ThreadPoolExecutor
    with ThreadPoolExecutor() as executor:
        results = list(executor.map(getData, getEventList()))
    return results
