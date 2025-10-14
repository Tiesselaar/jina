from src.tools.scraper_tools import myStrptime
from src.tools.scraper_tools import makeSoup, futureDate

# CALENDARS = ['theaterAmsterdam', 'classicalAmsterdam']

def formatTime(time_str):
    if '@' in time_str:
        return time_str.split('@')[1].strip(), ""
    return "11:00", " (Start time might be wrong, check the site!)"

def formatVenue(venue_address):
    if not venue_address:
        return "Ruigoord", "Ruigoord 76, 1047 HH Amsterdam"
    venue = venue_address.select_one('span.tribe-events-calendar-list__event-venue-title').text.strip()
    address = venue_address.select_one('span.tribe-events-calendar-list__event-venue-address').text.strip()
    if any([
        venue.lower() == 'in de kerk',
        venue.lower() == 'in het dorpshuis',
        'Ruigoord 76' in address,
    ]):
        return "Ruigoord", "Ruigoord 76, 1047 HH Amsterdam"
    if venue == "Theo's Theetuin":
        return "Theo's Theetuin", "Ruigoord, 1047 HH Amsterdam"
    if venue == "in de salon":
        return "Salon Ruigoord", "Ruigoord, 1047 HH Amsterdam"
    if "Kraggenburg" in address:
        return None, None
    raise ValueError(f"Unknown venue: {venue} at {address}")

def formatPrice(price):
    if price:
        return price.text.strip().lower().replace(' ', '').replace(',', '.').replace('gratis', 'free')
    return ""

def getData(event):
    venue, address = formatVenue(event.select_one('.tribe-events-calendar-list__event-venue'))
    if not venue:
        return None
    time, unknown_time = formatTime(event.select_one('header time .tribe-event-date-start').text)
    eventData = {
        'date': event.select_one('header time').get('datetime'),
        'time': time,
        'title': event.select_one('h3.tribe-events-calendar-list__event-title a').text.strip() + unknown_time,
        'venue': venue,
        'price': formatPrice(event.select_one('.tribe-events-c-small-cta__price')),
        'site': event.select_one('h3.tribe-events-calendar-list__event-title a').get('href'),
        'address': address
    }
    return eventData

def getEventList():
    url = 'https://ruigoord.nl/programma/lijst/pagina/'
    events = sum([
        makeSoup(url + str(page)).select('#content .tribe-events-calendar-list .tribe-events-calendar-list__event-row')
        for page in range(1, 4)
    ], [])
    return events

def bot():
    return map(getData, getEventList())
    # return (gig for event in getEventList() for gig in getData(event))
