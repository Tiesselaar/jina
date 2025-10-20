from src.tools.scraper_tools import myStrptime
from src.tools.scraper_tools import makeSeleniumSoup

CALENDARS = ["theaterAmsterdam", "classicalAmsterdam"]

def formatDate(dateString):
    dateString = " ".join(dateString.split()[:5])
    dateFormat = '%a %d %b \'%y %H:%M'
    date = myStrptime(dateString, dateFormat)
    return date.strftime('%Y-%m-%d'), date.strftime('%H:%M')

def getData(event):
    title, date_time = event.select('a > div > div > div')
    date, time = formatDate(date_time.select_one('div > div > div > div > div').text)
    eventData = {
        'date': date,
        'time': time,
        'title': title.select_one('div').text.strip(),
        'venue': "Podium Mozaïek",
        'price': "",
        'site': "https://www.podiummozaiek.nl" + event.select_one('a').get('href'),
        'address': "Bos en Lommerweg 191, 1055 DT Amsterdam"
    }
    if eventData['title'] == "dddd":
        return
    if "concert" in event.text.lower():
        yield {**eventData, 'calendar': 'classicalAmsterdam'}
    yield {**eventData, 'calendar': 'theaterAmsterdam'}

def getEventList():
    url = 'https://www.podiummozaiek.nl/programma/agenda'
    events = makeSeleniumSoup(url, 2).select('li[data-event-id]:not([data-event-id=""])')
    return events

def bot():
    return (gig for event in getEventList() for gig in getData(event))