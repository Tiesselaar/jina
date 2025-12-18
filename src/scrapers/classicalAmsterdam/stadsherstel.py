from src.tools.scraper_tools import myStrptime
from src.tools.scraper_tools import makeSoup, makeSeleniumSoup, futureDate
import datetime
import re

CALENDARS = ['classicalAmsterdam', 'theaterAmsterdam']

def formatDate(dateString):
    if len(dateString.split()) == 3:
        dateString += " " + str(datetime.date.today().year)
    dateString = dateString.replace('.', '')
    dateFormat = '%a %d %b %Y'
    date = myStrptime(dateString, dateFormat).date()
    return date.strftime('%Y-%m-%d')

def formatPrice(details):
    price = re.search(r'€ ?\d+([,.]\d\d?)?', details)
    if price:
        price_float = float(price[0].strip('€ ').replace(',','.'))
        if price_float.is_integer():
            price_float = int(price_float)
        return '€' + str(price_float)
    return ""

def getData(args):
    calendar, event = args
    site = event.select_one('a.grid-block').get('href')
    print(site)
    subsoup = makeSoup(site)
    tickets = subsoup.select_one(".agenda-speellijst > table.speellijst tbody").select('tr')
    for ticket in tickets:
        if not "Eonarium Genesis: Een Spectaculaire Lichtshow" == event.select_one('h2.grid-title').text:
            event_data = {
                'date': formatDate(ticket.select_one('td').text),
                'time': ticket.select('td')[1].text.split()[0],
                'title': event.select_one('h2.grid-title').text,
                'venue': ticket.select('td')[2].text.strip(),
                'price': formatPrice(subsoup.select_one('.agenda-detail-table').text),
                'site': site,
                'address': "Amsterdam"
            }
            yield {**event_data, 'calendar': calendar}
            if 'jazz' in event.text.lower() and calendar=='classicalAmsterdam':
                yield {**event_data, 'calendar': 'jazzAmsterdam'}

def getEventList():
    url = 'https://stadsherstel.nl/culturele-activiteiten/cultuuragenda?c='
    urls = {
        "classicalAmsterdam": url + "Muziek",
        "theaterAmsterdam": url + "Theater"
    }
    events = {
        calendar: makeSeleniumSoup(urls[calendar], 5).select('ol#agenda-list > li.grid-item')
        for calendar in urls
        }
    if len(events['classicalAmsterdam']) < 10:
        raise Exception("Fewer gigs than expected...")
    return events

# def bot():
#     events = getEventList()
#     return ({**gig, 'calendar': calendar} for calendar in events for event in events[calendar] for gig in getData(event))

from concurrent.futures import ThreadPoolExecutor

def bot():
    events = getEventList()
    all_events = [(calendar, event) for calendar in events for event in events[calendar]]
    with ThreadPoolExecutor() as executor:
        results = executor.map(getData, all_events)
    return (gig for sublist in results for gig in sublist)