from src.tools.scraper_tools import myStrptime
from src.tools.scraper_tools import makeSoup, futureDate
import re

def formatPrice(description):
    price = re.search(r'€ ?\d+([,.]\d\d)?', description)
    if price:
        return price[0].replace(' ', '')
    elif "gratis" in description.lower():
        return "free"
    else:
        return ""

def getData(event):
    site = event.select_one('header > h3.tribe-events-calendar-list__event-title > a').get('href')
    subsoup = makeSoup(site)
    genre_tags = subsoup.select_one('.tec-events-elementor-event-widget__categories').text
    description = subsoup.select_one('h4.elementor-heading-title').text.lower()
    if ("Concert" in genre_tags or "Orgelconcert" in genre_tags):
        return {
            'date': event.select_one('header > div > time').get('datetime'),
            'time': event.select_one('header > div > time > span.tribe-event-date-start').text.split()[-1],
            'title': event.select_one('header > h3.tribe-events-calendar-list__event-title > a').text.strip(),
            'venue': "Westerkerk",
            'price': formatPrice(subsoup.select_one('#tribe-events-pg-template').text),
            'site': site,
            'address': "Prinsengracht 281, 1016 GW Amsterdam"
        }

def getEventList():
    url = 'https://westerkerk.nl/evenementen/lijst/'
    events = makeSoup(url).select(
        '#content .tribe-events .tribe-events-calendar-list > .tribe-events-calendar-list__event-row'
    )
    return events

def bot():
    return map(getData, getEventList())
