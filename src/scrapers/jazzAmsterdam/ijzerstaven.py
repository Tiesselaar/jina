from src.tools.scraper_tools import myStrptime, makeSoup

CALENDARS = ['jazzAmsterdam', 'classicalAmsterdam']

def formatDate(dateString):
    dateString = " ".join(dateString.split()[:3])
    dateFormat = '%d %b %Y,'
    date = myStrptime(dateString, dateFormat).date()
    return date.strftime('%Y-%m-%d')

def getData(event):
    title = event.select_one('span[data-hook="ev-list-item-title"]').text
    event_data = {
        'date': formatDate(event.select_one('div[data-hook="date"]').text),
        'time': event.select_one('div[data-hook="date"]').text.split()[3],
        'title': title,
        'venue': "Salon de IJzerstaven",
        'price': "",
        'site': event.select_one('a[data-hook="ev-rsvp-button"]').get('href'),
        'address': "Bickersgracht 10, 1013 LE Amsterdam"
    }
    if "jazz" not in title.lower():
        yield {**event_data, 'calendar': 'classicalAmsterdam'}
    yield {**event_data, 'calendar': 'jazzAmsterdam'}

def getEventList():
    url = 'https://www.ijzerstaven.nl/agenda'
    events = makeSoup(url).select('#wix-events-widget li[data-hook="event-list-item"]')
    return events

def bot():
    return (gig for event in getEventList() for gig in getData(event))
