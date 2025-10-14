from src.tools.scraper_tools import myStrptime
from src.tools.scraper_tools import makeSoup, futureDate
import re

def formatDate(dateString):
    dateFormat = '%d %B %Y'
    date = myStrptime(dateString, dateFormat).date()
    return date.strftime('%Y-%m-%d')

def formatPrice(description):
    description = " ".join(description.split())
    price_search = re.search(r'1 concert: € ?\d+([,\.]\d\d?)?', description)
    if price_search:
        price = price_search[0].strip('1 concert: ')
        return price.replace(' ','').replace(',','.')
    price_search = re.search(r'prijs van € ?\d+([,\.]\d\d?)?', description)
    # if price_search:
    price = price_search[0].strip('prijs van')
    return price.replace(' ','').replace(',','.')

def getData(event):
    site = event.select_one('.wp_theatre_event_title a').get('href')
    description = makeSoup(site).select_one('main.content').text
    return {
        'date': formatDate(event.select_one('.wp_theatre_event_datetime .wp_theatre_event_startdate').text),
        'time': event.select_one('.wp_theatre_event_datetime .wp_theatre_event_starttime').text,
        'title': event.select_one('.wp_theatre_event_title a').text,
        'venue': "Uilenburgersjoel",
        'price': formatPrice(description),
        'site': site,
        'address': "Nieuwe Uilenburgerstraat 91, 1011 LM Amsterdam"
    }

def getEventList():
    url = 'https://www.uilenburgersjoel.nl/agenda/'
    events = makeSoup(url).select('main.content article .wp_theatre_event')
    return events

def bot():
    return map(getData, getEventList())
