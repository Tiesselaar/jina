from src.tools.scraper_tools import myStrptime
from src.tools.scraper_tools import makeSoup, futureDate
import re

CALENDARS = ['worldAmsterdam', 'jazzAmsterdam']

def formatDate(dateString):
    dateString += " 2024"
    dateFormat = '%A %d %B %Y'
    date = myStrptime(dateString, dateFormat).date()
    date = futureDate(date)
    return date.strftime('%Y-%m-%d')

def testDate(dateTimeLine):
    try:
        formatDate(dateTimeLine.select_one('span').text)
    except:
        return False
    return True


def formatTime(time):
    return re.search(r"\d\d:\d\d", time)[0]

def getData(event):
    eventData = {
        'date': formatDate(event[0].select_one('span').text),
        'time': formatTime(event[0].select('span')[1].text),
        'title': event[1].text.strip(),
        'venue': "Cancún",
        'price': "", # formatPrice(subsoup.select_one('.prijs').text),
        'site': "https://cancunamsterdam.nl/agenda/",
        'address': "Veelaan 15, 1019AP Amsterdam"
    }
    if "jazz" in event[-1].text.lower():
        yield {**eventData, 'calendar': 'jazzAmsterdam'}
    yield {**eventData, 'calendar': 'worldAmsterdam'}

def getEventList():
    url = 'https://cancunamsterdam.nl/agenda/'
    event_lines = makeSoup(url).select('.page-content h2')
    def next_genre_tag(x):
        for y in range(x + 1, len(event_lines)):
            if "GENRE :" in event_lines[y].text:
                return y
    events = [event_lines[x:next_genre_tag(x) + 1] for x in range(len(event_lines)) if testDate(event_lines[x])]
    return events

def bot():
    return (gig for event in getEventList() for gig in getData(event))