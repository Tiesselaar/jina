from src.tools.scraper_tools import myStrptime
from src.tools.scraper_tools import makeSoup, makeSeleniumSoup, futureDate
import re

def formatDate(dateString):
    dateString = dateString[:-7] + dateString[-5:]
    dateFormat = '%A, %B %d %Y'
    date = myStrptime(dateString, dateFormat).date()
    # date = futureDate(date)
    return date.strftime('%Y-%m-%d')

def formatPrice(description):
    try:
        price = re.search(r"Regulier:[  ]*€?[  ]*\d+(,\d\d?)?", description)[0]
    except:
        return ""
    price = "".join(price.split())
    price = float(price.replace('Regulier:','').replace('€','').replace(',','.'))
    return '€' + str(price)

def getData(event):
    site = event.get('href')
    description = makeSoup(site).select_one('article .entry-content').text
    return {
        'date': formatDate(event.select_one('span.eo-fullcalendar-screen-reader-text').text.strip()),
        'time': event.select_one('span.fc-time').text,
        'title': event.select_one('span.fc-title').text,
        'venue': "Dominicuskerk",
        'price': formatPrice(description),
        'site': site,
        'address': "Spuistraat 12A, 1012 TS Amsterdam"
    }

def getEventList():
    url = 'https://dominicusamsterdam.nl/agenda/'
    nextPage = "document.querySelector('.next-month').click()"
    events = sum(
        (
            makeSeleniumSoup(url, 2, page * [nextPage]).select('td.fc-event-container a.eo-event-cat-extern')
            for page in range(3)
        ), []
    )
    return events

def bot():
    return map(getData, getEventList())
