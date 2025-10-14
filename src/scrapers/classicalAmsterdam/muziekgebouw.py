from src.tools.scraper_tools import myStrptime
from src.tools.scraper_tools import makeSoup

CALENDARS = ['classicalAmsterdam', 'jazzAmsterdam']

def formatDate(dateString):
    dateFormat = '%a %d %b %Y'
    date = myStrptime(dateString, dateFormat).date()
    return date.strftime('%Y-%m-%d')

def formatPrice(price):
    if price:
        return "".join(price.text.split()).replace(',00','')
    return ""

def formatTitle(title, subtitle):
    if subtitle:
        return title + " - " + subtitle
    return title

def getData(event):
    time_tag = event.select_one('.top-date > span.time')
    if time_tag:
        return {
            'date': formatDate(event.select_one('.top-date > span.start').text.strip()),
            'time': time_tag.text.strip(),
            'title': formatTitle(event.select_one('h2.title').text.strip(),event.select_one('div.subtitle').text.strip()),
            'venue': "Muziekgebouw",
            'price': formatPrice(event.select_one('.price > button.pricePopoverBtn')),
            'site': "https://www.muziekgebouw.nl" + event.select_one('.descMetaContainer > a.desc').get('href'),
            'address': "Piet Heinkade 1, 1019 BR Amsterdam"
        }

def getSoup(calendar, page):
    url = 'https://www.muziekgebouw.nl/nl/agenda?genres%5B%5D={genre}&page={page}'
    genre_code = {
        "classicalAmsterdam": "",
        "jazzAmsterdam": "5"
    }
    return makeSoup(url.format(genre = genre_code[calendar], page = page))

def getEventList():
    events =  {
        calendar: [
            event
            for page in range(1,6)
            for event in getSoup(calendar, page).select('ul.listItems li.eventCard')]
        for calendar in CALENDARS
    }
    return events

def bot():
    events = getEventList()
    return (
        {**eventdatum, 'calendar': calendar}
            for calendar in events
            for event in events[calendar]
            for eventdatum in [getData(event)] if eventdatum
        )
