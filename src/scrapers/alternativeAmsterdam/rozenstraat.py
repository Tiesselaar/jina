from src.tools.scraper_tools import makeSoup

def getData(event):
    return {
        'date': event.select_one('time').get("datetime")[:10],
        'time': event.select_one('time').get("datetime")[11:16],
        'title': event.select_one('div').text,
        'venue': "Rozenstraat",
        'price': "",
        'site': event.get('href'),
        'address': "Rozenstraat 59, 1016 NN Amsterdam"
    }

def getEventList():
    url = 'https://www.rozenstraat.com/events/'
    events = makeSoup(url).select('.main .event-list:not(.m-archive) a.post-item-link')
    return events

def bot():
    return map(getData, getEventList())