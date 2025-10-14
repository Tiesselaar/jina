from src.tools.scraper_tools import myStrptime
from src.tools.scraper_tools import makeSoup, makeSeleniumSoup, futureDate
import re

def formatDate(dateString):
    dateFormat = '%d–%m–%Y'
    date = myStrptime(dateString, dateFormat).date()
    return date.strftime('%Y-%m-%d')

def formatTime(time):
    if time == "":
        return
    return time.split()[0].split('t/m')[0]

def formatAddress(address):
    lines = address.contents[1:]
    return ", ".join(x for x in map(lambda line: line.text, lines) if x).strip()


def formatPrice(price):
    price = re.search(r'\d+(,[(\d\d)-])? €', price)
    if price:
        return "€" + price[0].strip('€ ,-')
    else:
        return ""

def getData(event):
    site = event.select_one('.event-list-additional-info a.event-list-link').get('href')
    subsoup = makeSeleniumSoup(site, 2)
    time = formatTime(event.select('.event-list-date > p')[1].text)
    if time:
        return {
            'date': formatDate(event.select_one('.event-list-date > p > time').text),
            'time': time,
            'title': event.select_one('h3.event-list-title').text,
            'venue': subsoup.select_one('.event-calendar-location-container address > span').text,
            'price': formatPrice(subsoup.select_one('.event-calendar-fact-list').text),
            'site': site,
            'address': formatAddress(subsoup.select_one('.event-calendar-location-container address'))
        }

def getEventList():
    url = 'https://www.goethe.de/ins/nl/nl/ver.cfm#adress_IDtxt=Amsterdam&category_IDtxt=178929'
    # url = 'https://www.goethe.de/ins/nl/nl/ver.cfm'
    events = makeSeleniumSoup(url, 2).select_one('#event-list-js').select('li.event-item')
    return events

def bot():
    return map(getData, getEventList())
