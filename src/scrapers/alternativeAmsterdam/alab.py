from src.tools.scraper_tools import myStrptime
from src.tools.scraper_tools import makeSoup

CALENDARS = ['jazzAmsterdam', 'alternativeAmsterdam']

def formatDate(tags):
    tags = [tag.text for tag in tags if tag.text not in "–"]
    dateString = " ".join(tags)
    dateFormat = '%d %b %Y'
    date = myStrptime(dateString, dateFormat).date()
    return date.strftime('%Y-%m-%d')

# def formatTime(time):
#     # format time as '21:00'
#     return time

# def formatPrice(price):
#     # format price as '\u20ac12,50' (no space!)
#     price = price.replace(' ','')
#     return price


def format_info_lines(tags):
    info_lines = {}
    for tag in tags:
        key, value = tag.select('div')
        info_lines[key.text] = value.text.strip()
    return info_lines

def formatTime(time):
    return time.split('-')[0].replace('Vanaf', '').strip()

def formatPrice(price):
    if 'gratis' in price.lower():
        return 'free'
    if 'voor members' in price.lower():
        return ""
    return price


def getData(event):
    info_lines = format_info_lines(event.select('.event-info_wrapper a.event-item-info_wrapper'))
    event_data = {
        'date': formatDate(event.select('.event-date_wrapper div div')),
        'time': formatTime(info_lines['Tijd:']),
        'title': " - ".join(map(lambda x: x.text.strip(), event.select_one('.event-info_wrapper .event-title_wrapper :is(h3,h4)'))),
        'venue': "A Lab",
        'price': formatPrice(info_lines["Prijs:"]),
        'site': "https://www.a-lab.nl" + event.select_one('a').get('href'),
        'address': "Overhoeksplein 2, 1031 KS, Amsterdam"
    }
    yield {**event_data, 'calendar': 'alternativeAmsterdam'}
    if 'jazz' in event.text.lower():
        yield {**event_data, 'calendar': 'jazzAmsterdam'}

def getEventList():
    url = 'https://www.a-lab.nl/events'
    events = makeSoup(url).select('[data-w-tab="UPCOMING EVENTS"] .w-dyn-list .w-dyn-item')
    return events

def bot():
    # return map(getData, getEventList())
    return (gig for event in getEventList() for gig in getData(event))
