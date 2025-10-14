from src.tools.scraper_tools import myStrptime
from src.tools.scraper_tools import makeSoup
import re

# CALENDARS = ['theaterAmsterdam', 'classicalAmsterdam']

def formatDate(dateString):
    dateString = dateString.split()
    dateString[1] = dateString[1][:3]
    dateString = " ".join(dateString)
    dateFormat = '%d %b %Y'
    date = myStrptime(dateString, dateFormat).date()
    return date.strftime('%Y-%m-%d')

def getData(event):
    site = event.select_one('h3 a').get('href')
    description = makeSoup(site).select_one('#main .entry-content').text
    time = re.search(r'\d?\d[:.]\d\d', description)
    if not time:
        return
    return {
        'date': formatDate(event.select_one('h3 a').text.split('~')[0].strip()),
        'time': time[0].replace('.',':').rjust(5,'0'),
        'title': event.select_one('h3 a').text.split('~')[1].strip(),
        'venue': "Gamelanhuis",
        'price': "",
        'site': site,
        'address': "Veemkade 578, 1019 BL Amsterdam"
    }

def getEventList():
    url = 'https://www.gamelanhuis.nl/nieuws/'
    events = makeSoup(url).select('.panel-widget-style ul li.rpwe-li')
    return events

def bot():
    return map(getData, getEventList())
    # return (gig for event in getEventList() for gig in getData(event))
