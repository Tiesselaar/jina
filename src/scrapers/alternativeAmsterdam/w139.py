from src.tools.scraper_tools import makeSoup
import re

# CALENDARS = ['theaterAmsterdam', 'classicalAmsterdam']

def formatPrice(description):
    price = re.search(r"(Prijs|Toegangsprijs): €\d+", description)
    if price:
        return price[0].split()[1]
    "Prijs: EUR 5"
    price = re.search(r"(Prijs|Toegangsprijs): EUR \d+", description)
    if price:
        return "€" + price[0].split()[2]
    return ""

def getData(event):
    site = event.select_one('.event-thumb > a').get('href')
    subsoup = makeSoup(site)
    time = subsoup.select_one('time.event-time')
    if not time:
        return
    return {
        'date': event.select_one('time.event-date').get('datetime'),
        'time': time.get('datetime').split('T')[1][:5],
        'title': event.select_one('h3.event-title').text,
        'venue': "W139",
        'price': formatPrice(subsoup.select_one('.tribe_events').text),
        'site': site,
        'address': "Warmoesstraat 139, 1012 JB Amsterdam"
    }

def getEventList():
    url = 'https://w139.nl'
    events = makeSoup(url).select('.events.events-future > article.event')
    return events

def bot():
    from concurrent.futures import ThreadPoolExecutor
    with ThreadPoolExecutor() as executor:
        results = list(executor.map(getData, getEventList()))
    return results
