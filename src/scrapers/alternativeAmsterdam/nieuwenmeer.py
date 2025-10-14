from src.tools.scraper_tools import myStrptime
from src.tools.scraper_tools import makeSoup
import re

CALENDARS = ['alternativeAmsterdam', 'jazzAmsterdam']

def formatTime(event_text):
    event_text = event_text.lower()
    time = re.search(r'\d{1,2}[:.]\d{2} ?(am|pm)?', event_text)
    if time:
        time_str = time.group(0).replace('.', ':').replace(' ', '')
        if 'am' in time_str or 'pm' in time_str:
            return myStrptime(time_str, '%I:%M%p').strftime('%H:%M')
        else:
            return myStrptime(time_str, '%H:%M').strftime('%H:%M')
    time = re.search(r' \d{1,2} ?(am|pm)', event_text)
    if time:
        time_str = time.group(0).replace(' ', '')
        return myStrptime(time_str, '%I%p').strftime('%H:%M')
    return "11:00"

def getData(event):
    time = formatTime(event.text)
    wrong_time = " - Event time may be wrong, check the website" if time == "11:00" else ""
    eventData = {
        'date': "-".join(event.select_one('span.date').text.split(' - ')[0].strip().split('-')[::-1]),
        'time': formatTime(event.text),
        'title': event.select_one('a.title').text + wrong_time,
        'venue': "Nieuw en Meer",
        'price': "",
        'site': event.select_one('a.title').get('href'),
        'address': "Oude Haagseweg 53A1, 1066 BV Amsterdam"
    }
    yield {**eventData, 'calendar': 'alternativeAmsterdam'}
    if "jazz" in event.text.lower():
        yield {**eventData, 'calendar': 'jazzAmsterdam'}

def getEventList():
    url = 'https://nieuwenmeer.nl/en/agenda/'
    events = makeSoup(url).select('#agenda > .itemcontainer > article')
    return events

def bot():
    return (gig for event in getEventList() for gig in getData(event))
