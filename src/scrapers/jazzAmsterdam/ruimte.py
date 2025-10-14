from src.tools.scraper_tools import myStrptime, makeSoup
import re

def formatDate(date):
    dateFormat = '%b %d, %Y'
    my_date = myStrptime(date, dateFormat)
    return my_date.strftime('%Y-%m-%d')

def formatPrice(fullText):
    priceSearch = re.search(r'tickets \d*-\d*', fullText)
    if priceSearch:
        return "€" + priceSearch[0].split()[1]
    return ""

def getData(event):
    site = event.select('.vc_gitem-link')[0].get('href')
    subsoup = makeSoup(site)
    eventData = {
        'date': formatDate(subsoup.select('.us_custom_c5cc888c')[1].text),
        'time': subsoup.select_one('.us_custom_62ae7985').text,
        'title': event.select_one('.vc_gitem-link').text,
        'venue': "De Ruimte",
        'price': formatPrice(subsoup.select_one('#page-content').text),
        'site': site,
        'address': 'Sexyland World, Noordwal 1, 1021 PX Amsterdam'
    }
    return(eventData)

def getEventList():
    url='https://www.cafederuimte.nl/'
    events = makeSoup(url).select('.vc_custom_1645697310396')
    return events

def bot():
    return map(getData, getEventList())


