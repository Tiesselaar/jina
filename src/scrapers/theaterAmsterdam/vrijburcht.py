from src.tools.scraper_tools import myStrptime, futureDate, makeSoup

CALENDARS = ['theaterAmsterdam', 'jazzAmsterdam']


def formatDate(dateString):
    dateString += " 2024"
    dateFormat = '%A %d %B %Y'
    date = futureDate(myStrptime(dateString, dateFormat).date())
    return date.strftime('%Y-%m-%d')

def formatTime(time):
    return time.replace(' uur','').replace('.', ':')

def formatPrice(price):
    if price:
        price = price.text
    else:
        return ""
    price = price.replace('Entree ','').strip()
    price = price.replace(',-', '').replace(',00', '')
    price = price.replace(',50', ',5').replace(',5', ',50')
    return price

def getData(event):
    if not event.select_one('div.entry-text'):
        return
    eventData = {
        'date': formatDate(event.select_one('div.entry-text header.entry-header div.entry-meta span.date time.entry-date').text),
        'time': formatTime(event.select_one('div.entry-text header.entry-header div.entry-meta span.date span.time').text),
        'title': event.select_one('div.entry-text header.entry-header h1.entry-title a').text,
        'venue': "Theater Vrijburcht",
        'price': formatPrice(event.select_one('div.entry-text footer.event div.event-extra-info span.event-price')),
        'site': event.select_one('div.entry-text header.entry-header h1.entry-title a').get('href'),
        'address': "Jan Olphert Vaillantlaan 143, 1086 XZ Amsterdam"
    }
    if (
        "jazz" in event.text.lower() or
        "impro" in event.text.lower() and
        "muziek" in event.text.lower()
        ):
        yield { **eventData , 'calendar': 'jazzAmsterdam' }
    yield { **eventData, 'calendar': 'theaterAmsterdam' }
    
def getEventList():
    venue_name = 'vrijburcht'
    urls = ('https://theatervrijburcht.nl/programma/?pno={}'.format(x) for x in range(1,5))
    eventMaps = map(lambda url: makeSoup(url).select('section.event-list > article.event'), urls)
    events = sum(eventMaps,[])
    return events

def bot():
    return (gig for event in getEventList() for gig in getData(event))


