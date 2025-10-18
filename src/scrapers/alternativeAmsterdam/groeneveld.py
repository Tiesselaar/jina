from src.tools.scraper_tools import makeSoup

# CALENDARS = ['theaterAmsterdam', 'classicalAmsterdam']

def formatTime(date_time):
    time = date_time.select_one('.tribe-event-time')
    if time:
        return time.text.strip()
    time = date_time.select_one('.tribe-event-date-start')
    if time:
        return time.text.split('@')[-1].strip()

def formatVenue(venue):
    if venue:
        return venue.text.strip() \
            .replace('Buitenterrein', '') \
            .replace('Gehele terrein', '') \
            .replace('Het Machinegebouw', 'Het Groene Veld (Machinegebouw)')
    else:
        return "Het Groene Veld"

def formatAddress(address):
    if address:
        address = address.text.strip()
        if 'of via G.J. Scheurleerweg 212c' in address:
            return 'G.J. Scheurleerweg 212c, Amsterdam'
        return address.replace('Amsterdam Noord', 'Amsterdam') \
            .replace(' , ', ', ')
    else:
        return "G.J. Scheurleerweg 212c, 1027 BA Amsterdam"


def getData(event):
    return {
        'date': event.select_one('header time').get('datetime'),
        'time': formatTime(event.select_one('header time')),
        'title': event.select_one('h3.tribe-events-calendar-list__event-title a').text.strip(),
        'venue': formatVenue(event.select_one('address .tribe-events-calendar-list__event-venue-title')),
        'price': "",
        'site': event.select_one('h3.tribe-events-calendar-list__event-title a').get('href'),
        'address': formatAddress(event.select_one('address .tribe-events-calendar-list__event-venue-address')) 
    }

def getEventList():
    url = 'https://hetgroeneveld.amsterdam/agenda/'
    events = makeSoup(url).select('.tribe-events-calendar-list .tribe-common-g-row.tribe-events-calendar-list__event-row')
    return events

def bot():
    return map(getData, getEventList())
    # return (gig for event in getEventList() for gig in getData(event))
