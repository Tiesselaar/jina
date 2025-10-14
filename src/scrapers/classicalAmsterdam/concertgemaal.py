from src.tools.scraper_tools import myStrptime
from src.tools.scraper_tools import makeSoup


def formatDate(dateString):
    dateFormat = '%d %b %Y'
    date = myStrptime(dateString.split(',')[0], dateFormat).date()
    return date.strftime('%Y-%m-%d')

def formatPrice(price_options):
    for price_option in price_options:
        if "regulier" in price_option.text.lower():
            price = price_option.select_one('[data-hook="price"]').text
            return "".join(price.replace(',','.').replace('.00','').split())
    return ""

def getData(event):
    site = event.select_one('a[data-hook$="title"]').get('href')
    subsoup = makeSoup(site)
    return {
        'date': formatDate(subsoup.select_one('p[data-hook="event-full-date"]').text),
        'time': subsoup.select_one('p[data-hook="event-full-date"]').text.split()[3],
        'title': event.select_one('a[data-hook$="title"]').text,
        'venue': "Concertgemaal",
        'price': formatPrice(subsoup.select('li[data-hook="ticket-pricing-option"]')),
        'site': site,
        'address': "Landsmeerderdijk 213, 1035 PV Amsterdam"
    }

def getEventList():
    url = 'https://www.concertgemaal.nl/concerten'
    events = makeSoup(url).select(
        '#wix-events-widget[data-hook="EVENTS_ROOT_NODE"] ul > li')
    return events

def bot():
    return map(getData, getEventList())
