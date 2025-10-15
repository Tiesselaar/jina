from src.tools.scraper_tools import myStrptime
from src.tools.scraper_tools import makeSoup, futureDate
import re

CALENDARS = ['jazzAmsterdam', 'classicalAmsterdam']


def formatDate(dateString):
    dateFormat = '%d %B %Y'
    date = myStrptime(dateString, dateFormat).date()
    return date.strftime('%Y-%m-%d')

def formatTime(text):
    time = re.search(r'Show time: \d\d.\d\du', text)[0][-6:-1].replace('.', ':')
    return time

def getData(event):
    site = event.select_one('h3.t-entry-title > a').get('href')
    subsoup = makeSoup(site)
    description = " ".join(map(lambda x: x.text, subsoup.select('.uncode_text_column')))
    event_data = {
        'date': formatDate(event.select_one('span.t-entry-date').text),
        'time': formatTime(event.select_one('.t-entry-excerpt > p').text),
        'title': event.select_one('h3.t-entry-title > a').text,
        'venue': "Studio 150",
        'price': "free" if "De toegang is gratis" in description else "",
        'site': site,
        'address': "Zwanenplein 34, 1021 CM Amsterdam"
    }
    if "jazz" in description.lower():
        yield {**event_data, 'calendar': 'jazzAmsterdam'}
    else:
        yield {**event_data, 'calendar': 'classicalAmsterdam'}

def getEventList():
    url = 'https://studio150.nl/concerts/'
    events = makeSoup(url).select('.uncode-post-table > .tmb-table')
    return events

def bot():
    return (gig for event in getEventList() for gig in getData(event))