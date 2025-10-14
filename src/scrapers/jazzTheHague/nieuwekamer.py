from src.tools.scraper_tools import myStrptime
from src.tools.scraper_tools import makeSeleniumSoup, futureDate

def address(venue):
    return {
    "Musicon": "Soestdijksekade 345, 2574 AL Den Haag",
    "Podium aan Zee": "Keizerstraat 58, 2584 BK Den Haag",
    "Leonardo Royal Hotel Promenade": "Van Stolkweg 1, 2585 JL Den Haag",
    "Brasserie Amare": "Spuiplein 150, 2511 DG Den Haag",
    "Pulchri Studio": "Lange Voorhout 15, 2514 EA Den Haag"
    }[venue]

def formatDateTime(dateString):
    dateFormat = '%a %d %b %Y – %H:%M'
    date = myStrptime(dateString, dateFormat)
    return date.strftime('%Y-%m-%d'), date.strftime('%H:%M')

def formatPrice(price):
    price = price.replace(',00','')
    price = "".join(price.split())
    return price

def getData(event):
    date, time = formatDateTime(event.select_one('.wp_theatre_event_startdate').text)
    venue = event.select_one('.wp_theatre_event_venue').text
    priceElement = event.select_one('.wp_theatre_event_prices')
    eventData = {
        'date': date,
        'time': time,
        'title': event.select_one('.wp_theatre_event_title').text,
        'venue': venue,
        'price': formatPrice(priceElement.text) if priceElement else "",
        'site': event.select_one('a').get('href'),
        'address': address(venue)
    }
    return eventData

def getEventList():
    url = 'https://podiumdenieuwekamer.nl/concert-agenda/'
    events = makeSeleniumSoup(url).select('.wp_theatre_event')
    return events

def bot():
    return map(getData, getEventList())
