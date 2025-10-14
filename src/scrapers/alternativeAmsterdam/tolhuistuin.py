from src.tools.scraper_tools import myStrptime, makeSoup, makeSeleniumSoup
import re

CALENDARS = {'alternativeAmsterdam', 'jazzAmsterdam', 'theaterAmsterdam'}

def formatDate(date):
    date = " ".join(date.split())
    dateFormat = '%a %A %d %b, %y'
    my_date = myStrptime(date, dateFormat)
    return my_date.strftime('%Y-%m-%d')

def formatTime(sidebarInfo, site):
    timeSearch = re.search(r"Tijd\n\d\d:\d\d",sidebarInfo)
    if timeSearch:
        return timeSearch[0][-5:]
    timeSearch = re.search(r"\d?\d:\d\d",sidebarInfo)
    if timeSearch:
        return timeSearch[0]
    raise Exception("No time! " + site)

def formatPrice(sidebarInfo):
    try:
        entreeLine = sidebarInfo.split("Entree")[1].strip().split('\n')[0]
        price = re.search(r'\d*([.,]\d+)?', entreeLine)[0]
    except:
        return ""
    return "€{}".format(price).replace(".",",")

def getData(event):
    site = event.get('href')
    subsoup = makeSoup(site)
    sidebarInfo = subsoup.select_one('.sidebar__information').text
    eventData = {
        'date': formatDate(subsoup.select_one('.sidebar__event-date').text),
        'time': formatTime(sidebarInfo, site),
        'title': event.select_one('h3.event__title').text,
        'venue': "Tolhuistuin",
        'price': formatPrice(sidebarInfo),
        'site': site,
        'address': "IJpromenade 2, 1031 KT Amsterdam"
    }
    if "jazz" in event.text.lower():
        yield {**eventData, 'calendar': 'jazzAmsterdam'}
    if "theater" in sidebarInfo.lower():
        yield {**eventData, 'calendar': 'theaterAmsterdam'}
    yield {**eventData, 'calendar': 'alternativeAmsterdam'}


def getEventList():
    url = 'https://tolhuistuin.nl/agenda'
    scripts = ('document.querySelector(\'a[aria-label="load more events"]\').click()' for i in range(5))
    events = makeSeleniumSoup(url, 0, scripts).select('li.event > a')
    return events

def bot():
    return (gig for event in getEventList() for gig in getData(event))