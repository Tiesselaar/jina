from src.tools.scraper_tools import myStrptime
from src.tools.scraper_tools import makeSoup, futureDate


def formatDate(dateString):
    dateFormat = '%d %B %Y - %H:%M'
    date = myStrptime(dateString, dateFormat).date()
    return date.strftime('%Y-%m-%d')

# def formatTime(time):
#     # format time as '21:00'
#     return time

# def formatPrice(price):
#     # format price as '\u20ac12,50' (no space!)
#     price = price.replace(' ','')
#     return price

def getData(data):
    site, event = data
    return {
        'date': formatDate(event.select_one('time > .tribe-event-date-start').text),
        'time': event.select_one('time > .tribe-event-time').text,
        'title': event.select_one('h4.tribe-events-calendar-list__event-title > a').text.strip(),
        'venue': event.select_one('address .tribe-events-calendar-list__event-venue-title').text.strip(),
        'price': "",
        'site': site,
        'address': event.select_one('address .tribe-events-calendar-list__event-venue-address').text.strip()
    }

def getEventList():
    url = 'https://www.pknduivendrecht.nl/agenda/'
    tags = [
        'tag/opera',
        'tag/concert',
        'tag/muziek-lezing',
        'tag/muzieklezing',
        'categorie/kleinoot/'
    ]
    def make_url_pair(concert):
        return [
            concert.select_one('h4.tribe-events-calendar-list__event-title > a').get('href'),
            concert
        ]
    
    events = dict(make_url_pair(concert) for tag in tags for concert in makeSoup(url + tag).select(
        '.tribe-events-calendar-list article.tribe-events-calendar-list__event')
    )
    return ([link, events[link]] for link in events.keys())

def bot():
    return map(getData, getEventList())
