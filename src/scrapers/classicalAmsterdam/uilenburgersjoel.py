from src.tools.scraper_tools import myStrptime
from src.tools.scraper_tools import makeSoup
import re

def formatDate(dateString):
    dateFormat = '%d %B %Y'
    date = myStrptime(dateString, dateFormat).date()
    return date.strftime('%Y-%m-%d')

def formatPrice(price):
    if price:
        return '€' + price.text.replace('vanaf', '').strip().replace(',','.').replace('.00','')
    else:
        return ""

def getData(event):
    site = event.select_one('.wp_theatre_event_title a').get('href')
    subsoup = makeSoup(site)
    return {
        'date': formatDate(event.select_one('.wp_theatre_event_datetime .wp_theatre_event_startdate').text),
        'time': event.select_one('.wp_theatre_event_datetime .wp_theatre_event_starttime').text,
        'title': event.select_one('.wp_theatre_event_title a').text,
        'venue': "Uilenburgersjoel",
        'price': formatPrice(subsoup.select_one('.wp_theatre_event_tickets > .wp_theatre_event_prices')),
        'site': site,
        'address': "Nieuwe Uilenburgerstraat 91, 1011 LM Amsterdam"
    }

def getEventList():
    url = 'https://www.uilenburgersjoel.nl/agenda/'
    events = makeSoup(url).select('main.content article .wp_theatre_event')
    return events

def bot():
    return map(getData, getEventList())
