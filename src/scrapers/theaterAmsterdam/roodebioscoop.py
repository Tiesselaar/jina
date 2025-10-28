from src.tools.scraper_tools import myStrptime, makeSoup, futureDate
from ..jazzAmsterdam.__musicians__ import musicians
import re

CALENDARS = ['theaterAmsterdam', 'jazzAmsterdam', 'classicalAmsterdam']

def formatDate(dateString):
    dateString += " 2020"
    dateFormat = '%a %d %b %Y'
    date = futureDate(myStrptime(dateString.strip(), dateFormat).date())
    return date.strftime('%Y-%m-%d')

def formatTime(timePrice):
    return timePrice.split('|')[0].replace('uur','').strip()

def formatPrice(timePrice):
    price = "".join(timePrice.split('|')[1:])
    price = price.replace(',00','').replace(' ','')
    return price

def getData(event):
    site = event.select_one('.agenda-item-title a').get('href')
    print(site)
    description = makeSoup(site).select_one('.show-detail').text
    eventData = {
        'date': formatDate(event.select_one('.agenda-item-day').text),
        'time': formatTime(event.select_one('.agenda-item-time').text),
        'title': event.select_one('.agenda-item-title').text.strip().title(),
        'venue': "De Roode Bioscoop",
        'price': formatPrice(event.select_one('.agenda-item-time').text),
        'site': site,
        'address': 'Haarlemmerplein 7, 1013 HP Amsterdam'
    }
    yield {**eventData, 'calendar':'theaterAmsterdam'}
    if (
        any(keyword in description.lower() for keyword in ["jazz", "improv", "bossa nova"]) or
        any(musician in description for musician in musicians)
    ):
        yield {**eventData, 'calendar':'jazzAmsterdam'}
    if (
        any(re.search(keyword, description.lower()) for keyword in [r"klassieke? "])
    ):
        yield {**eventData, 'calendar':'classicalAmsterdam'}

def getEventList():
    venue_name = 'roodebioscoop'
    url = 'https://www.roodebioscoop.nl/programma'
    events = makeSoup(url).select('.agenda-item')
    return events

def bot():
    from concurrent.futures import ThreadPoolExecutor
    with ThreadPoolExecutor() as executor:
        return (
            gig
            for gigs in executor.map(lambda event: list(getData(event)), getEventList())
            for gig in gigs
        )