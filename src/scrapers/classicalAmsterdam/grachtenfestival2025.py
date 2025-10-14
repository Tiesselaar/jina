from src.tools.scraper_tools import myStrptime
from src.tools.scraper_tools import makeSoup, futureDate

CALENDARS = ['classicalAmsterdam', 'jazzAmsterdam']

def formatDate(dateString):
    dateFormat = '%d-%m-%Y'
    date = myStrptime(dateString, dateFormat).date()
    return date.strftime('%Y-%m-%d')

def getLocation(info_boxes):
    for box in info_boxes:
        location_link = box.get('hx-get') or ""
        if "/locatie/" in location_link:
            location_link = "https://www.grachtenfestival.nl" + location_link
            break
    if not location_link:
        return None, None
    location_soup = makeSoup(location_link)
    return (location_soup.select_one('#main h1').text, location_soup.select_one('#content+div > a').text.strip())
    
def getPrice(info_boxes, subsoup):
    if "gratis" in info_boxes[-1].text.lower():
        return "free"
    return ""

def getData(event_calendar):
    event, calendar = event_calendar
    site = "https://www.grachtenfestival.nl" + event.select_one('a').get('hx-get').split('?')[0]
    subsoup = makeSoup(site)
    info_boxes = subsoup.select('#main h6 + div > a')
    venue, address = getLocation(info_boxes)
    price = getPrice(info_boxes, subsoup)
    if not venue:
        print("no location...")
        return
    return {
        'date': formatDate(info_boxes[0].text.strip()),
        'time': info_boxes[1].text.split('-')[0].strip(),
        'title': "Grachtenfestival: " + subsoup.select_one('#main h1').text,
        'venue': venue,
        'price': price,
        'site': site,
        'address': address,
        'calendar': calendar,
    }

def getEventList():
    genres = {
        "jazzAmsterdam": "1",
        "classicalAmsterdam": "3",
    }
    url = 'https://www.grachtenfestival.nl/programma-2025?genre='
    events = [[event, calendar] for calendar in CALENDARS for event in makeSoup(url + genres[calendar]).select('.zoekresultaat')]
    return events

def bot():
    return map(getData, getEventList())
    # return (gig for event in getEventList() for gig in getData(event))
