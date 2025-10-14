from src.tools.scraper_tools import myStrptime
from src.tools.scraper_tools import makeSoup, makeSeleniumSoup
import re

CALENDARS = ['classicalAmsterdam', 'jazzAmsterdam']

def formatDate(dateString):
    dateFormat = '%d %B %Y'
    date = myStrptime(dateString, dateFormat).date()
    return date.strftime('%Y-%m-%d')

def formatLocation(location):
    if "Luther Museum Amsterdam, Nieuwe Keizersgracht 570" in location:
        return "Luther Museum", "Nieuwe Keizersgracht 570, 1018 VG Amsterdam"
    if "Dr. Sarphatihuis, Roetersstraat 2, 1018 WC Amsterdam" in location:
        return "Dr. Sarphatihuis", "Roetersstraat 2, 1018 WC Amsterdam"
    if "SOOP, Nieuwe Kerkstraat 124, 1018 VM Amsterdam" in location:
        return "SOOP", "Nieuwe Kerkstraat 124, 1018 VM Amsterdam"
    if location.strip() == "":
        return "Luther Museum", "Nieuwe Keizersgracht 570, 1018 VG Amsterdam"

    else:
        print(location)
        raise Exception('Unknown location')


def getData(event):
    description = event.text.lower()
    if not ("tentoonstelling" not in description
            or "muziek" in description
            or "concert" in description
            or "muzikale" in description
            or "jazz" in description):
        return
    site, = [link.get('href') for link in event.select('a.button') if "Lees meer" in link.text]
    try:
        tickets, = [link.get('href') for link in event.select('a.button') if "Tickets" in link.text]
        price = re.search(r'€[  ]?\d+([\.,]\d\d)?', makeSeleniumSoup(tickets, 1).text)[0]
        price = price.replace(',', '.').replace(' ', '').replace(' ','').replace('.00', '')
    except Exception as e:
        # raise e
        price = ""
    venue, address = formatLocation(event.select_one('.locatie').text)
    event_data =  {
        'date': formatDate(event.select_one('.evenement-datum').text.strip()),
        'time': event.select_one('.evenement-tijd').text.split('-')[0].strip(),
        'title': event.select_one('.tile-title-box h2').text,
        'venue': venue,
        'price': price,
        'site': site,
        'address': address
    }
    if "jazz" in description:
        yield {**event_data, "calendar": "jazzAmsterdam"}
    else:
        yield {**event_data, "calendar": "classicalAmsterdam"}


def getEventList():
    url = 'https://luthermuseum.nl/nl/agenda'
    events = makeSoup(url).select('.tiles-parent .tile')
    return events


def bot():
    return (gig for event in getEventList() for gig in getData(event))