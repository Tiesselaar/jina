from src.tools.scraper_tools import myStrptime
from src.tools.scraper_tools import makeSoup, futureDate
from bs4 import Tag

CALENDARS = ['jazzAmsterdam', 'classicalAmsterdam']

def formatDate(dateString):
    dateString = " ".join(dateString.split())
    dateFormat = '%A %d. %m. %Y'
    date = myStrptime(dateString, dateFormat).date()    
    return date.strftime('%Y-%m-%d')

def getData(event: Tag):
    all_lines = event.get_text('\n', True).replace('\u200b', '')
    lines = [line for line in all_lines.split('\n') if line]
    event_data = {
        'date': formatDate(lines[0] + " " + lines[1]),
        'time': lines[2].replace(".",":").replace('at ',''),
        'title': " ".join(lines[3].split()),
        'venue': "Opus Amsterdam",
        'price': "€16",
        'site': "https://www.opusamsterdam.com/calendar1",
        'address': "Westerdok 610, 1013 BV Amsterdam"
    }
    yield {**event_data, 'calendar': 'classicalAmsterdam'}
    if "jazz" in event.text.lower():
        yield {**event_data, 'calendar': 'jazzAmsterdam'}

def getEventList():
    url = 'https://www.opusamsterdam.com/calendar1'
    sections = makeSoup(url).select('.fe-block .sqs-block-content .sqs-html-content:has(h3+h3)')
    return sections

def bot():
    return (gig for event in getEventList() for gig in getData(event))