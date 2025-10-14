from src.tools.scraper_tools import myStrptime
from src.tools.scraper_tools import makeSoup, futureDate


def formatDate(dateString):
    dateString = " ".join(dateString.split()[:3])
    dateFormat = '%d %B %Y'
    date = myStrptime(dateString, dateFormat).date()
    return date.strftime('%Y-%m-%d')

def formatPrice(subsoup):
    if "Tickets beschikbaar over" in subsoup.text or "Geen tickets beschikbaar!" in subsoup.text:
        return ""
    price = subsoup.select_one('#tickets article .price').text
    price = "".join(price.split()).replace('*','').replace(',','.').replace('.00','')
    return price

def getData(event):
    site = event.select_one('h3 > a').get('href')
    subsoup = makeSoup(site)
    return {
        'date': formatDate(event.select_one('.kioskinfo').text),
        'time': event.select_one('.kioskinfo').text.split()[3],
        'title': "Huiskamerconcert: " + event.select_one('h3 > a').text,
        'venue': "Rozengracht 55H",
        'price': formatPrice(subsoup),
        'site': site,
        'address': "Amsterdam"
    }

def getEventList():
    url = 'https://shop.ikbenaanwezig.nl/kiosk/Rozengracht55H'
    events = makeSoup(url).select('.container li.kiosk')
    return events

def bot():
    return map(getData, getEventList())
