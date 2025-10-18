from src.tools.scraper_tools import myStrptime
from src.tools.scraper_tools import makeSoup, futureDate

CALENDARS = ['popAmsterdam', 'jazzAmsterdam']

def formatDate(dateString):
    dateString += ".2024"
    dateFormat = '%d.%m.%Y'
    date = myStrptime(dateString, dateFormat).date()
    date = futureDate(date)
    return date.strftime('%Y-%m-%d')

def formatTime(infoLines):
    details = {
        line.select('div')[0].text.strip(': '): line.select('div')[1].text for line in infoLines
    }
    return details['show']

def formatPrice(priceString):
    if "gratis" in priceString:
        return "free"
    if "donatie" in priceString:
        return "pwyw"
    priceString = priceString.strip().replace(',', '.').replace('*', '').replace(' ', '')
    if int(priceString.split('.')[1]) == 0:
        priceString = priceString.split('.')[0]
    return priceString

def getData(event):
    site = "https://www.cinetol.nl" + event.select_one('a').get('href')
    subsoup = makeSoup(site)

    time = formatTime(subsoup.select('.section_event-info-text .div-block-5 .section_event-door-wrapper')).strip()
    if time == "t.b.a.":
        return None
    
    eventData = {
        'date': formatDate(event.select_one('.event_date-wrapper .event_date-flex').text),
        'time': time,
        'title': event.select_one('.event_text-wrapper div[fs-cmsfilter-field="zoeknaam"]').text.strip(),
        'venue': "Cinetol",
        'price': formatPrice(subsoup.select_one('.ticket .ticket_prices-wrapper+.div-block-4').text),
        'site': site,
        'address': "Tolstraat 182, 1074VM Amsterdam",
    }

    yield {**eventData, 'calendar': "popAmsterdam"}
    if "jazz" in event.text.lower():
        yield {**eventData, 'calendar': "jazzAmsterdam"}

def getEventList():
    url = 'https://www.cinetol.nl/programma'
    events = makeSoup(url).select('.section_program .programma .event-item')
    return events

def bot():
    return (gig for event in getEventList() for gig in getData(event))
