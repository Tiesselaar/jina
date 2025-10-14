from src.tools.scraper_tools import myStrptime
from src.tools.scraper_tools import makeSoup, futureDate
import re

# CALENDARS = ['theaterAmsterdam', 'classicalAmsterdam']

def formatDate(dateString):
    dateString += " 2024"
    dateFormat = '%a %d %B %H:%M %Y'
    date = myStrptime(dateString, dateFormat).date()
    date = futureDate(date)
    return date.strftime('%Y-%m-%d')

def formatPrice(price):
    price = "".join(price.split()[:2])
    if re.match(r"€\d+(,\d+)?", price):
        return price.replace(',','.').replace('.00','')
    return ""

def getData(event):
    remark = event.select_one('.wp_theatre_event_remark').text
    return {
        'date': formatDate(event.select_one('.wp_theatre_event_datetime').text),
        'time': event.select_one('.wp_theatre_event_datetime').text.split()[-1],
        'title': event.select_one('.wp_theatre_event_title a').text + (f" ({remark.lower()})" if remark else ""),
        'venue': "Polanentheater",
        'price': formatPrice(event.select_one('.wp_theatre_event_aangepaste_prijs').text),
        'site': event.select_one('.wp_theatre_event_title a').get('href'),
        'address': "Polanenstraat 174, 1013 WC, Amsterdam"
    }

def getEventList():
    url = 'https://polanentheater.nl/agenda/'
    events = makeSoup(url).select('.container .wp_theatre_event')[:50]
    if len(events) < 10:
        raise Exception('Fewer events than expected!!!')
    return events

def bot():
    return map(getData, getEventList())