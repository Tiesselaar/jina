from src.tools.scraper_tools import makeSoup

def getData(event):
    return {
        'date': event.select_one('header time').get('datetime'),
        'time': event.select_one('header time > .tribe-event-date-start').text.split('@')[1].strip(),
        'title': event.select_one('h4 > a').get('title').strip(),
        'venue': "GROND",
        'price': "",
        'site': event.select_one('h4 > a').get('href'),
        'address': "Bijdorpstraat 1, 1096 AP Amsterdam"
    }

def getEventList():
    url = 'https://grond.community/events/list/'
    events = makeSoup(url).select('.tribe-events-calendar-list__event-row')
    return events

def bot():
    return map(getData, getEventList())