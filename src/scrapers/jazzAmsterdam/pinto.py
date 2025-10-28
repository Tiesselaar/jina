from src.tools.scraper_tools import myStrptime, makeSoup, futureDate
import re

CALENDARS = ['jazzAmsterdam', 'classicalAmsterdam']

def formatDate(dateString):
    dateString = " ".join(dateString.split())
    dateFormat = '%d %B %Y'
    dateString = dateString + " 2020"
    date = futureDate(myStrptime(dateString, dateFormat).date(), 60)
    return date.strftime('%Y-%m-%d')

def formatPrice(content):
    priceSearch = re.search(r"Entree € \d+(,\d+)?", content)
    if priceSearch:
        return "€" + priceSearch[0].split()[-1]
    return("")

def getData(event):
    site = "https://huisdepinto.nl" + event.get('href')
    print(site)
    description = makeSoup(site).select_one('.content').text
    eventData = {
        'date': formatDate(event.select_one('.content .date-time .date').text),
        'time': event.select_one('.content .date-time .time').text.strip(),
        'title': event.select_one('.content h3.title').text.strip(),
        'venue': "Huis de Pinto",
        'price': formatPrice(description),
        'site': site,
        'address': "St. Antoniesbreestraat 69, 1011 HB Amsterdam"
        }
    if any(keyword in description.lower() for keyword in ['impro', 'jazz','pintotonics']):
        yield {**eventData, 'calendar': 'jazzAmsterdam'}
    if any(keyword in description.lower() for keyword in ['matinee', 'concert']):
        yield {**eventData,'calendar': 'classicalAmsterdam'}


def getEventList():
    url = 'https://huisdepinto.nl/programma/'
    events = makeSoup(url).select('.cards a.card')
    return events

from concurrent.futures import ThreadPoolExecutor

def bot():
    events = getEventList()
    with ThreadPoolExecutor() as executor:
        results = executor.map(lambda event: list(getData(event)), events)
    return (gig for gigs in results for gig in gigs)
