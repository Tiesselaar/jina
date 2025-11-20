from src.tools.scraper_tools import myStrptime
from src.tools.scraper_tools import makeSoup, futureDate

CALENDARS = ['alternativeAmsterdam', 'jazzAmsterdam']

def formatDate(dateString):
    if len(dateString.split()) == 3:
        dateString += " 2024"
    dateFormat = '%A, %d %B %Y'
    date = myStrptime(dateString, dateFormat).date()
    date = futureDate(date)
    return date.strftime('%Y-%m-%d')

def formatTime(event):
    if event.select('.date-display-start'):
        return event.select_one('.date-display-start').text
    return event.select_one('.date-display-single').text

def formatPrice(details):
    if "Price: free" in details:
        return "free"
    else:
        return ""

def getData(event):
    site = "https://radar.squat.net" + event.select_one('td > div > a').get('href')
    details = makeSoup(site).select_one("#content").text
    eventData = {
        'date': formatDate(event.select_one('td .date').text),
        'time': formatTime(event),
        'title': event.select_one('td > div > a').text,
        'venue': "Takland",
        'price': formatPrice(details),
        'site': site,
        'address': "Taksteeg 6, 1012BP Amsterdam"
    }
    if (
        "JⒶZZ" in event.text or
        "jazz" in event.text.lower() or
        "herrie" in event.text.lower()
    ):
        yield {**eventData, 'calendar': 'jazzAmsterdam'}

def getEventList():
    url = 'https://radar.squat.net/en/amsterdam/takland-vrijstraat/events'
    events = makeSoup(url).select('#content tbody tr')[:10]
    return events

def bot():
    return (gig for event in getEventList() for gig in getData(event))
