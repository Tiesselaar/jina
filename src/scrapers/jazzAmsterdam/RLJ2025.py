from src.tools.scraper_tools import myStrptime
from src.tools.scraper_tools import makeSoup, futureDate

from bs4 import BeautifulSoup


def formatDate(dateString):
    dateString += " 2025"
    dateFormat = '%d %B %Y'
    date = myStrptime(dateString, dateFormat).date()
    return date.strftime('%Y-%m-%d')

def formatPrice(price, site):
    if "gratis toegang" in price.lower():
        return "free"
    subsoup = makeSoup(site)
    details = subsoup.select(".event-details p")
    for detail in details:
        if "Prijs:" in detail.text:
            prijs_text = detail.text
            prijs_text = prijs_text.replace("Prijs:", "")
            prijs_text = prijs_text.replace('€', '')
            prijs_text = prijs_text.replace(',-', '')
            prijs_text = prijs_text.split()[0].replace(",",".")
            return prijs_text
    return ""

def getData(event):
    site = event.select_one('.program-hm-sc-title h3 a').get('href')
    return {
        'date': formatDate(" ".join(event.select_one('.program-hm-sc-date').text.split())),
        'time': event.select_one('.program-hm-sc-time').text.split('-')[0].strip(),
        'title': "Red Light Jazz: " + event.select_one('.program-hm-sc-title h3 a').text,
        'venue': event.select_one('.program-hm-sc-location span').text,
        'price': formatPrice(event.select_one('.program-hm-sc-ticket').text, site),
        'site': site,
        'address': event.select_one('.program-hm-sc-address').text.replace(" |", ","),
    }

def getEventList():
    url = 'https://redlightjazz.com/programma/?date=all'
    events = makeSoup(url).select('#date0 .program-hm-sc-item')
    return events

def bot():
    return map(getData, getEventList())
