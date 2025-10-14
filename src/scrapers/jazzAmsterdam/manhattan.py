from src.tools.scraper_tools import myStrptime, futureDate, makeSoup
import re

def formatDate(event):
    rawDate = event.select_one('.elementor-widget-container > p').text.strip()
    dateString = rawDate[0:-2] + " 2020"
    dateFormat = '%B %d %Y'
    date = futureDate(myStrptime(dateString, dateFormat).date(), 90)
    return date.strftime('%Y-%m-%d')

def formatTime(eventInfo):
    time = re.search(r'Music starts at \d\d:\d\d', eventInfo)[0][-5:]
    return time

def formatTitle(event):
    performing = event.select_one('h6').text.strip()
    if performing == "Performing:":
        ensembleName = event.select_one('h6+:is(p, h5, h6, div)').text.strip()
        return ensembleName
    else:
        raise Exception('irregular format')

def getData(event):
    if "Add to agenda" in event.text:
        return {
            'date': formatDate(event),
            'time': formatTime(event.text),
            'title': formatTitle(event),
            'venue': "Manhattan Bar",
            'price': "",
            'site': 'https://manhattanbar.nl/events/live-music-nights-on-thursdays/',
            'address': "George Gershwinlaan 103, 1082 MT Amsterdam"
        }

def getEventList():
    url = 'https://manhattanbar.nl/events/live-music-nights-on-thursdays/'
    soup = makeSoup(url)
    events = soup.select('#content > div.page-content > div.elementor > section.elementor-section:not(.elementor-hidden-desktop)')
    return events

def bot():
    return map(getData, getEventList())