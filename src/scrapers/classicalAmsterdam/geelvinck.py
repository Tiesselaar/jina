from src.tools.scraper_tools import myStrptime
from src.tools.scraper_tools import makeSoup, futureDate
import re

CALENDARS = ['jazzAmsterdam', 'classicalAmsterdam']

def formatDate(dateString):
    dateString = " ".join(dateString.split()[:3])
    dateFormat = '%d %b %Y,'
    date = myStrptime(dateString, dateFormat).date()
    return date.strftime('%Y-%m-%d')

def address(venue):
    if venue == "Luther Museum, Amsterdam":
        return "Nieuwe Keizersgracht 570, 1018 VG Amsterdam"
    if venue == "Pianola Museum, Amsterdam":
        return "Westerstraat 106, 1015 MN Amsterdam"
    return "Amsterdam"

def formatPrice(description):
    price_search = re.search(r'Toegang:? ?\d+([,.]\d\d?)?', description)
    if price_search:
        price_float = float(price_search[0].strip('Toegang: ').replace(',','.'))
        if price_float.is_integer():
            price_float = int(price_float)
        return '€' + str(price_float)
    return ""

def getData(event):
    site = event.select_one('header h2.entry-title a').get('href')
    subsoup = makeSoup(site)
    try:
        venue = event.select_one('.view-card-content-waar').text.strip()
    except Exception as e:
        if 'jazz at the pianola' in event.select_one('header h2.entry-title a').text.lower():
            venue = "Pianola Museum, Amsterdam"
    if not ", Amsterdam" in venue:
        return
    
    event_data = {
        'date': formatDate(event.select_one('.view-card-content-wanneer').text),
        'time': event.select_one('.view-card-content-wanneer').text.split()[-1].replace('.',':'),
        'title': event.select_one('header h2.entry-title a').text,
        'venue': venue.replace(', Amsterdam', ''),
        'price': formatPrice(subsoup.select_one('#main').text),
        'site': site,
        'address': address(venue)
    }
    if 'jazz' in event.text.lower():
        return {**event_data, 'calendar': 'jazzAmsterdam'}
    else:
        return {**event_data, 'calendar': 'classicalAmsterdam'}


def getEventList():
    url = 'https://geelvinck.nl/agenda/concerten-en-events/'
    events = makeSoup(url).select('#concerten > div > article')
    return events

def bot():
    return map(getData, getEventList())
