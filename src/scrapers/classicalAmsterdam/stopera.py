from src.tools.scraper_tools import myStrptime
from src.tools.scraper_tools import makeSeleniumSoup, futureDate
import re

def formatDate(dateString):
    dateString += " 2024"
    dateFormat = '%A %d %B %Y'
    date = myStrptime(dateString, dateFormat).date()
    date = futureDate(date)
    return date.strftime('%Y-%m-%d')

def price_location(ticket):
    price = re.search(r'€ \d*,\d\d', ticket)
    if price:
        return price[0], None
    elif re.search('Amsterdam', ticket):
        return None, ticket.replace('Amsterdam', '').strip(', ')
    else:
        return None, None


def getData(event):
    site = 'https://www.operaballet.nl' + event.select_one('a.programCard__button').get('href')
    subsoup = makeSeleniumSoup(site)
    tickets = subsoup.select('#tickets .ticket__content')
    for ticket in tickets:
        price, location = price_location(ticket.select_one('.ticket__price-location').text)
        if price or location:
            yield {
                'date': formatDate(ticket.select_one('.ticket__title').text),
                'time': ticket.select_one('.ticket__time').text[:5],
                'title': event.select_one('.programCard__content .programCard__category').text + ": " +
                        event.select_one('.programCard__content .programCard__title').text,
                'venue': location or "Nationale Opera & Ballet",
                'price': price or "",
                'site': site,
                'address': "Amsterdam" if location else "Amstel 3, 1011 PN Amsterdam"
            }

def getEventList():
    url = 'https://www.operaballet.nl/programma?page='
    events = sum((makeSeleniumSoup(url + str(i)).select('article.programCard') for i in range(3)), [])
    events = list({
        event.select_one('a.programCard__button').get('href'): event
        for event in events
    }.values())
    return events

def bot():
    return sum([list(x) for x in map(getData, getEventList())], [])
