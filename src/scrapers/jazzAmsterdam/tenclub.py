from src.tools.scraper_tools import myStrptime, makeSoup
import re

def formatDate(dateString):
    dateString = dateString.replace('st','').replace('nd','').replace('rd','').replace('th','')
    dateFormat = '%d %B %Y'
    date = myStrptime(dateString, dateFormat).date()
    return date.strftime('%Y-%m-%d')

def formatTime(eventText):
    timeSearch = re.search(r"([Pp]rogram(ma)?|[Ss]tart)( lecture| of meditation)?:? \d?\d[:.]\d\d", eventText)
    if timeSearch:
        return timeSearch[0].split()[-1].replace('.',':')
    timeSearch = re.search(r"\d?\d[:.]\d\d [Ss]tart program", eventText)
    if timeSearch:
        return timeSearch[0].split()[0].replace('.',':')
    timeSearch = re.search(r"[Oo]pen:? \d?\d[:.]\d\d", eventText)
    if timeSearch:
        return timeSearch[0].split()[-1].replace('.',':')

def formatPrice(eventText):
    priceSearch = re.findall(r'€ ?\d*[.,]?\d?\d?', eventText)
    if priceSearch:
        return priceSearch[-1].replace(' ', '').replace(',','.').replace('.00','')
    return ""

def getData(event):
    if (
        'jazz' in event.text.lower() or
        'pablo castillo' in event.text.lower()
        ):
        site = event.select_one('a').get('href')
        subsoup = makeSoup(site)
        eventData = {
            'date': formatDate(event.select_one('.dce-meta-wrapper').text),
            'time': formatTime(subsoup.text),
            'title': event.select_one('h3.elementor-heading-title').text,
            'venue': "Tenclub",
            'price': formatPrice(subsoup.text),
            'site': site,
            'address': 'Nes 116, 1012 KE Amsterdam'
        }
        if eventData['time'] == None:
            raise Exception('Can\'t find time')
        return eventData

def getEventList():
    venue_name = 'tenclub'
    url = 'https://tenclub.nl/events/'
    events = makeSoup(url).select('article')
    return events

def bot():
    from concurrent.futures import ThreadPoolExecutor
    with ThreadPoolExecutor() as executor:
        results = list(executor.map(getData, getEventList()))
    return results



