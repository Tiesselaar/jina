from src.tools.scraper_tools import myStrptime
from src.tools.scraper_tools import makeSoup


def formatDate(dateString):
    dateFormat = '%A %d %B %Y'
    date = myStrptime(dateString, dateFormat).date()
    return date.strftime('%Y-%m-%d')

def getData(event):
    site = event.select_one('a[class!="kaarten"][href^="https://dedillewijn.nl/voorstelling"]').get('href')
    subsoup = makeSoup(site)
    return {
        'date': formatDate(event.select_one('.date').text),
        'time': subsoup.select_one('.time').text.split()[1],
        'title': event.select_one('.artiest').text + " | " + event.select_one('.title').text,
        'venue': "Theater De Dillewijn (Ankeveen)",
        'price': subsoup.select_one('.price').text.split()[1],
        'site': site,
        'address': "Stichts End 57, 1244 PL Ankeveen"
    }

def getEventList():
    url = 'https://dedillewijn.nl/voorstellingen/jazz/'
    events = makeSoup(url).select('.voorstellingen section')
    return events

def bot():
    return map(getData, getEventList())