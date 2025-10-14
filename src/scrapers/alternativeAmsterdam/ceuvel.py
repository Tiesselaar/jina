from src.tools.scraper_tools import myStrptime, makeSoup

CALENDARS = ['alternativeAmsterdam', 'jazzAmsterdam', 'popAmsterdam']

def formatDate(date_string):
    date_format = '%d %B %Y'
    date = myStrptime(date_string, date_format).date()
    return date.strftime('%Y-%m-%d')

def formatPrice(price):
    if 'donatie' in price.lower():
        return 'tips'
    price = price.split('Toegang:')[-1].strip()
    price = price.replace(',-', '').replace('Free', 'free')
    if price != 'free':
        price = '€' + price
    return price

def getData(event):
    site = event.select_one('a').get('href')
    subsoup = makeSoup(site)
    eventData = {
        'date': formatDate(subsoup.select_one('.panel-body h2').text.strip()),
        'time': event.select_one('.event-data .entry-date').text.split('-')[0].strip().rjust(5,'0'),
        'title': event.select_one('.event-details .event-title').text.strip().title(),
        'venue': "De Ceuvel",
        'price': formatPrice(event.select_one('.thumb .event-meta').text),
        'site': site,
        'address': 'Korte Papaverweg 2, 1032 KB Amsterdam'
    }
    event_description = subsoup.select_one('article.event').text.lower()
    if 'jazz' in event_description:
        yield { **eventData, 'calendar': 'jazzAmsterdam' }
    if any(keyword in event_description for keyword in ['muziek', 'music', 'concert', 'session']):
        yield { **eventData, 'calendar': 'popAmsterdam' }
    yield { **eventData, 'calendar': 'alternativeAmsterdam' }


def getEventList():
    venue_name = 'ceuvel'
    url = 'https://deceuvel.nl/nl/events/'
    events = makeSoup(url).select('.row.event-normal.event-preview')
    return events

def bot():
    return (gig for event in getEventList() for gig in getData(event))
