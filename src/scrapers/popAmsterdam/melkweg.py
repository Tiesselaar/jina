from src.tools.scraper_tools import makeSoup
from datetime import datetime
from zoneinfo import ZoneInfo

CALENDARS = ['popAmsterdam', 'clubAmsterdam', 'jazzAmsterdam']

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

def format_datetime(date_time): ## 2025-11-15T20:15:00.000000Z
    dt = datetime.fromisoformat(date_time.replace("Z", "+00:00"))
    return dt.astimezone(ZoneInfo("Europe/Amsterdam")).isoformat()
    

def getData(event):
    site = "https://www.melkweg.nl" + event.select_one('a').get('href')
    subsoup = makeSoup(site)
    date_time = format_datetime(subsoup.select_one('time').get("datetime"))
    eventData = {
        'date': date_time[:10],
        'time': date_time.split('T')[1][:5],
        'title': event.select_one('h3[class^="styles_event-compact__title"]').text, 
        'venue': "Melkweg",
        'price': formatPrice(subsoup),
        'site': site,
        'address': "Lijnbaansgracht 234A, 1017 PH Amsterdam"
    }
    category = getattr(event.select_one('a > div > ul > li > span'), 'text', '').strip()
    if "jazz" in event.text.lower():
        yield {**eventData, 'calendar': 'jazzAmsterdam'}
    if category == "Club":
        yield {**eventData, 'calendar': 'clubAmsterdam'}
    else:
        yield {**eventData, 'calendar': 'popAmsterdam'}


def getEventList():
    url = 'https://www.melkweg.nl/en/agenda/'
    return makeSoup(url).select('div[data-element="agenda"] ol[class^="styles_event-list-day"] > li')

def bot():
    from concurrent.futures import ThreadPoolExecutor
    with ThreadPoolExecutor() as executor:
        return (
            gig
            for gigs in executor.map(lambda event: list(getData(event)), getEventList())
            for gig in gigs
        )