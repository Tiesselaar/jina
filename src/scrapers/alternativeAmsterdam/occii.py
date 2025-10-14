from src.tools.scraper_tools import myStrptime
from src.tools.scraper_tools import makeSoup, futureDate
import re

CALENDARS = ['alternativeAmsterdam', 'jazzAmsterdam']

def formatDate(dateString):
    dateString = " ".join(dateString.split()[:3]) + " 2024"
    dateFormat = '%A, %B %d %Y'
    date = myStrptime(dateString, dateFormat).date()
    date = futureDate(date, 30)
    return date.strftime('%Y-%m-%d')

def formatPrice(details):
    price = re.search(r"Damage: \d* euro", details)
    if price:
        price = "€" + price[0].split()[1]
        return price
    price = re.search(r"Damage: €\d*", details)
    if price:
        price = price[0].split()[1]
        return price
    if re.search(r"Damage: Free", details):
        return "free"
    return ""

def getData(event):
    site = event.select_one('h3.occii-event-link a').get('href')
    event_details = makeSoup(site).select_one('#occii-single-event .occii-event-details').text
    eventData = {
        'date': formatDate(event.select_one('.occii-event-times').text),
        'time': event.select_one('.occii-event-times').text[-5:],
        'title': event.select_one('h3.occii-event-link a').text.lower(),
        'venue': "OCCII",
        'price': formatPrice(event_details),
        'site': site,
        'address': "Amstelveenseweg 134, 1075 XL Amsterdam"
    }
    if "jazz" in event_details.lower():
        yield {**eventData, 'calendar': 'jazzAmsterdam'}
    yield {**eventData, 'calendar': 'alternativeAmsterdam'}


def getEventList():
    url = 'https://occii.org/events/'
    events = makeSoup(url).select('.occii-event-display')
    return events

def bot():
    return (gig for event in getEventList() for gig in getData(event))