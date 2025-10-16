from src.tools.scraper_tools import myStrptime, futureDate, makeSoup
from bs4 import Tag

def formatDate(dateString):
    dateFormat = '%A %d %B %Y'
    date = myStrptime(dateString, dateFormat)
    return date.strftime('%Y-%m-%d')


def format_address(venue):
    if venue == "Wester-Amstel":
        return "Amsteldijk Noord 55, 1183 TE Amstelveen"
    else:
        raise Exception('Unknown venue')

def getData(event: Tag):
    info = event.select_one('ul.ha-post-info')
    date, time, venue = [item.text.strip() for item in info.select('li')]
    if 'jazz' in event.text.lower():
        eventData = {
            'date': formatDate(date),
            'time': time.replace(' uur', ''),
            'title': event.select_one('h4.elementor-heading-title').text.strip(),
            'venue': venue,
            'price': "",
            'site': "https://wester-amstel.nl/agenda/",
            'address': format_address(venue),
        }
        return eventData

def getEventList():
    URL = 'https://wester-amstel.nl/agenda/'
    events = makeSoup(URL).select('h4.elementor-heading-title')
    return [event.parent.parent.parent for event in events]

def bot():
    return map(getData, getEventList())


