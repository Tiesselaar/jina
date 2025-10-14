from src.tools.scraper_tools import myStrptime
from src.tools.scraper_tools import makeSoup, futureDate

CALENDARS = ['popAmsterdam', 'jazzAmsterdam']

def formatPrice(subsoup):
    button_text = subsoup.select_one('div[class^="styles_event-header__content_"]').text
    if "Free" in button_text:
        return "free"
    if "Sold out" in button_text:
        return "s.o."
    try:
        price_text = subsoup.select_one('li[class^="styles_ticket-prices__price-label"]').text
        return "".join(price_text.split()[:2])
    except:
        print('no price')
    return ""

def getData(event):
    site = "https://www.melkweg.nl" + event.select_one('a').get('href')
    print(site)
    subsoup = makeSoup(site)
    eventData = {
        'date': subsoup.select_one('time').get("datetime")[:10],
        'time': subsoup.select_one('time').get("datetime")[11:16],
        'title': event.select_one('h3[class^="styles_event-compact__title"]').text, 
        'venue': "Melkweg",
        'price': formatPrice(subsoup),
        'site': site,
        'address': "Lijnbaansgracht 234A, 1017 PH Amsterdam"
    }
    if "jazz" in event.text.lower():
        yield {**eventData, 'calendar': 'jazzAmsterdam'}
    yield {**eventData, 'calendar': 'popAmsterdam'}


def getEventList():
    url = 'https://www.melkweg.nl/en/agenda/'
    return makeSoup(url).select('div[data-element="agenda"] ol[class^="styles_event-list-day"] > li')

def bot():
    return (gig for event in getEventList() for gig in getData(event))