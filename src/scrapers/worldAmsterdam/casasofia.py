from src.tools.scraper_tools import makeSoup

def getData(event):
    try:
        price = event.select_one('.tribe-events-c-small-cta__price').text.strip().lower()
    except:
        price = ""
    return {
        'date': event.select_one('header time').get('datetime'),
        'time': event.select_one('header time > .tribe-event-date-start').text.split("@")[1].strip(),
        'title': event.select_one('h3 > a').get('title'),
        'venue': "Casa Sofia",
        'price': price,
        'site': event.select_one('h3 > a').get('href'),
        'address': "Louwesweg 6G, 1066 EC Amsterdam"
    }

def getEventList():
    url = 'https://www.casasofia.nl/evenementen/'
    events = makeSoup(url).select('.tribe-events-calendar-list__event-row')
    return events

def bot():
    return map(getData, getEventList())
