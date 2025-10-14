from src.tools.scraper_tools import myStrptime
from src.tools.scraper_tools import makeSoup, futureDate

# CALENDARS = ['theaterAmsterdam', 'classicalAmsterdam']

def formatDate(dateString):
    dateString = dateString.replace('.', '')
    dateString += " 2024"
    dateFormat = '%a %d %b %Y'
    date = myStrptime(dateString, dateFormat).date()
    date = futureDate(date)
    return date.strftime('%Y-%m-%d')

def formatTime(sub_event, subsoup):
    data_tab_id = '#' + sub_event.get('data-tab')
    list_items = subsoup.select_one(data_tab_id).select('ul li')
    for hook in ["Aanvang", "Deuren"]:
        for item in list_items:
            if hook in item.contents[0]:
                return item.select_one('span').text.split()[0]
    # print('No time')
    return
    # raise Exception('No time: ' + str(list_items))

def getData(event):
    site = event.select_one('a').get('href')
    # print(site)
    subsoup = makeSoup(site)
    sub_events = subsoup.select('#timetable > div > button')
    for sub_event in sub_events:
        time = formatTime(sub_event, subsoup)
        if time:
            yield {
                'date': formatDate(sub_event.contents[0]),
                'time': time,
                'title': event.select_one('label').contents[0].strip(),
                'venue': "AFAS Live",
                'price': "",
                'site': site,
                'address': "Johan Cruijff Boulevard 590, 1101 DS Amsterdam"
            }

def getEventList():
    url = 'https://www.afaslive.nl/agenda'
    events = makeSoup(url).select('.agenda-container article')[:15]
    event_urls = [event.select_one('a').get('href') for event in events]
    for i in range(len(events) - 1, 0 - 1, -1):
        if event_urls[i] in event_urls[:i]:
            events.pop(i)
    return events

def bot():
    return (gig for event in getEventList() for gig in getData(event))