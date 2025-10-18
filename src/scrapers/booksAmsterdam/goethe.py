from src.tools.scraper_tools import myStrptime
from src.tools.scraper_tools import makeSoup, makeSeleniumSoup
import re

CALENDARS = ['booksAmsterdam', 'classicalAmsterdam', 'jazzAmsterdam']

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

def format_venue(venue):
    if venue == "Goethe-Institut Amsterdam":
        return "Goethe-Institut"
    if venue == "Goethe-Institut Niederlande":
        return "Goethe-Institut"
    return venue

def getData(event):
    site = event.select_one('.event-list-additional-info a.event-list-link').get('href')
    subsoup = makeSeleniumSoup(site, 2)
    time = formatTime(event.select('.event-list-date > p')[1].text)
    if not time:
        return
    event_data = {
        'date': formatDate(event.select_one('.event-list-date > p > time').text),
        'time': time,
        'title': event.select_one('h3.event-list-title').text,
        'venue': format_venue(subsoup.select_one('.event-calendar-location-container address > span').text),
        'price': formatPrice(subsoup.select_one('.event-calendar-fact-list').text),
        'site': site,
        'address': formatAddress(subsoup.select_one('.event-calendar-location-container address'))
    }
    yield {**event_data, 'calendar': 'booksAmsterdam'}
    if 'jazz' in event.text.lower():
        yield {**event_data, 'calendar': 'jazzAmsterdam'}
    if 'concert' in event.text.lower() or 'concert' in event.text.lower():
        yield {**event_data, 'calendar': 'classicalAmsterdam'}


def getEventList():
    url = 'https://www.goethe.de/ins/nl/nl/ver.cfm#adress_IDtxt=Amsterdam'
    # url = 'https://www.goethe.de/ins/nl/nl/ver.cfm'
    events = makeSeleniumSoup(url, 2).select_one('#event-list-js').select('li.event-item')
    return events

def bot():
    return (gig for event in getEventList() for gig in getData(event))