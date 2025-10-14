from src.tools.scraper_tools import myStrptime, makeSoup

CALENDARS = ['classicalAmsterdam', 'jazzAmsterdam']

def formatDate(dateTimeString):
    dateFormat = '%A %d %B %Y %H:%M'
    date = myStrptime(dateTimeString, dateFormat)
    return date.strftime('%Y-%m-%d'), date.strftime('%H:%M')

def getData(event):
    eventTitle = event.select_one(':scope a h2.listitem-title').text
    eventDate, eventTime = formatDate(event.select_one(':scope a p.listitem-date-full').text)
    eventData = {
        'date': eventDate,
        'time': eventTime,
        'title': eventTitle,
        'venue': "Orgelpark",
        'price': "\u20ac20",
        'site': event.select_one(':scope > a').get('href'),
        'address': 'Gerard Brandtstraat 28, 1054 JK Amsterdam'
    }
    if 'jazz' in eventTitle.lower():
        yield { **eventData, 'calendar': 'jazzAmsterdam' }
    yield { **eventData, 'calendar': 'classicalAmsterdam' }
            
def getEventList():
    url = 'https://www.orgelpark.nl/agenda'
    events = makeSoup(url).select('.placeholder .listitems article.listitem')
    return events

def bot():
    return (gig for event in getEventList() for gig in getData(event))