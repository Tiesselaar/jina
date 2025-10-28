from src.tools.scraper_tools import myStrptime
from src.tools.scraper_tools import makeSoup, makeSeleniumSoup, futureDate

import re

CALENDARS = ['theaterAmsterdam', 'jazzAmsterdam']

def formatDate(dateString):
    dateString = dateString.split('-')[0].strip()
    dateString += " 2024"
    dateFormat = '%a %d %b %Y'
    date = myStrptime(dateString, dateFormat).date()
    date = futureDate(date)
    return date.strftime('%Y-%m-%d')

def formatPrice(rows):
    price = ""
    for row in rows:
        if ("Rang 1:" == row.select_one('td').text.strip() or
            "Tickets:" == row.select_one('td').text.strip()):
            price = row.select_one('td:nth-child(2)').text.strip()
            break
    price = price.replace(' ','').replace(',','.').replace('.00','')
    return price

def getData(event):
    site = 'https://meervaart.nl/' + event.select_one('a').get('href')
    print(site)
    subsoup = makeSoup(site)
    date_time_tags = [date for date in subsoup.select('span.h6') if re.search(r'\d:\d\d', date.text.strip())]
    for date in date_time_tags:
        event_data = {
            'date': formatDate(date.text.strip()),
            'time': date.text.strip().split(' ')[-1],
            'title': " // ".join(map(lambda tag: tag.text.strip(), event.select(':is(h3, h5)'))),
            'venue': "Meervaart Theater",
            'price': formatPrice(subsoup.select('tr')),
            'site': site,
            'address': "Meer en Vaart 300, 1068 LE Amsterdam",
        }
        if "jazz" in event.text.lower():
            yield {**event_data, 'calendar': 'jazzAmsterdam'}
        yield {**event_data, 'calendar': 'theaterAmsterdam'}

def getEventList():
    js = """
    Array.from(document.querySelectorAll('span.cursor-pointer')).filter(
      el => el.textContent.trim() === 'Meer voorstellingen')[0].click();
    """
    url = 'https://meervaart.nl/agenda'
    events = makeSeleniumSoup(url, 1, scripts=[js]).select('#agenda-items-container article')
    return events

def bot():
    from concurrent.futures import ThreadPoolExecutor
    with ThreadPoolExecutor() as executor:
        return (
            gig
            for gigs in executor.map(lambda event: list(getData(event)), getEventList())
            for gig in gigs
        )