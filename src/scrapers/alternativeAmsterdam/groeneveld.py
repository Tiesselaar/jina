from src.tools.scraper_tools import makeSoup

# CALENDARS = ['theaterAmsterdam', 'classicalAmsterdam']

def formatTime(date_time):
    time = date_time.select_one('.tribe-event-time')
    if time:
        return time.text.strip()
    time = date_time.select_one('.tribe-event-date-start')
    if time:
        return time.text.split('@')[-1].strip()

def formatAddress(address):
    if 'of via G.J. Scheurleerweg 212c' in address:
        return 'G.J. Scheurleerweg 212c, Amsterdam'
    return address.replace('Amsterdam Noord', 'Amsterdam') \
        .replace(' , ', ', ')



def getData(event):
    return {
        'date': event.select_one('header time').get('datetime'),
        'time': formatTime(event.select_one('header time')),
        'title': event.select_one('h3.tribe-events-calendar-list__event-title a').text.strip(),
        'venue': event.select_one('address .tribe-events-calendar-list__event-venue-title').text.strip() \
            .replace('Buitenterrein', '') \
            .replace('Gehele terrein', '') \
            .replace('Het Machinegebouw', 'Het Groene Veld (Machinegebouw)'),
        'price': "",
        'site': event.select_one('h3.tribe-events-calendar-list__event-title a').get('href'),
        'address': formatAddress(event.select_one('address .tribe-events-calendar-list__event-venue-address').text.strip()) 
    }

def getEventList():
    url = 'https://hetgroeneveld.amsterdam/agenda/'
    events = makeSoup(url).select('.tribe-events-calendar-list .tribe-common-g-row.tribe-events-calendar-list__event-row')
    return events

def bot():
    return map(getData, getEventList())
    # return (gig for event in getEventList() for gig in getData(event))
