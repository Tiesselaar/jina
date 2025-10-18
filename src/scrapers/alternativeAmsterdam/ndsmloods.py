from src.tools.scraper_tools import myStrptime
from src.tools.scraper_tools import makeSoup, futureDate

CALENDARS = ['theaterAmsterdam', 'alternativeAmsterdam', 'jazzAmsterdam']

def formatDate(dateString):
    date_vector = dateString.split()[:4]
    for suffix in ["th", "st", "nd", "rd"]:
        date_vector[2] = date_vector[2].replace(suffix, '')
    dateString = " ".join(date_vector)
    dateFormat = '%A, %B %d, %Y'
    date = myStrptime(dateString, dateFormat)
    return date.strftime('%Y-%m-%d')

def formatLocation(location_string):
    if "NDSM Theater" in location_string:
        return "NDSM Theater", "Scheepsbouwkade 4-6, 1033 WM Amsterdam, Nederland"
    if "NDSM FUSE" in location_string.upper():
        return "NDSM FUSE", "NDSM-Plein 29, 1033 WC Amsterdam"
    if location_string in ["NDSM Loods", "NDSM-Loods", "NDSM Terrein", "NDSM TERREIN", "-", "WUNDERKAMMER"]:
        return "NDSM-Loods", "NDSM-Plein 85, 1033 WC Amsterdam"
    raise Exception("Unknown location: " + location_string)

def getData(event):
    venue, address = formatLocation(event.select_one('.wpem-event-location').text.strip())
    title = event.select_one('.wpem-event-title h3.wpem-heading-text').text
    time = event.select_one('.wpem-event-date-time-text').text.split('-')[0].split('@')
    if title == "Cotton Jazz on Tour (again) – wekelijks jazzconcerten elke zaterdag NDSM Theater/Café":
        return
    if len(time) != 2:
        return
    else:
        time = time[1].strip()
    eventData = {
        'date': formatDate(event.select_one('.wpem-event-date-time-text').text),
        'time': time,
        'title': title,
        'venue': venue,
        'price': "",
        'site': event.select_one('a.wpem-event-action-url').get('href'),
        'address': address
    }
    yield {**eventData, 'calendar': 'alternativeAmsterdam'}
    if eventData['venue'] == 'NDSM Theater':
        yield {**eventData, 'calendar': 'theaterAmsterdam'}
    if 'jazz' in event.text.lower():
        yield {**eventData, 'calendar': 'jazzAmsterdam'}

def getEventList():
    url = 'https://www.ndsmloods.nl/evenementen/'
    events = makeSoup(url).select('#event-listing-view > .wpem-event-box-col')
    return events

def bot():
    # return map(getData, getEventList())
    return (gig for event in getEventList() for gig in getData(event))
