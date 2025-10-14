from src.tools.scraper_tools import myStrptime, makeSoup
import re

def formatDate(date):
    dateFormat = '%d%b %Y'
    my_date = myStrptime(date, dateFormat)
    return my_date.strftime('%Y-%m-%d')

def formatTime(eventInfo):
    time = re.search(r'Tijd:\d\d:\d\d', eventInfo)[0][-5:]
    return time

def getData(event):
    site = event.select_one('div.tour-place span.sub-head a').get('href')
    subsoup = makeSoup(site)
    if 'jazz' in subsoup.select_one('#page .container').text.lower():
        return {
            'date': formatDate(event.select_one('p.tour-date').text),
            'time': formatTime(subsoup.select_one('#meta-wrap ul.item-meta').text),
            'title': event.select_one('div.tour-place span.sub-head a').text,
            'venue': event.select_one('div.tour-place span.main-head span').text,
            'price': "",
            'site': site,
            'address': event.select_one('div.tour-place span.main-head meta').get('content')
        }

def getEventList():
    venue_name = 'liveineurope'
    url = 'https://liveineurope.nl/events/'
    events = makeSoup(url).select_one('div.events ul.tour-dates').select('li.group')
    return events

def bot():
    return map(getData, getEventList())