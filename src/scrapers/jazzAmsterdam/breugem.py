from src.tools.scraper_tools import myStrptime
from src.tools.scraper_tools import makeSoup, futureDate

import re

def formatDate(dateString):
    dateString += " 2024"
    dateFormat = '%A %d %B %H:%M %Y'
    datetime = myStrptime(dateString, dateFormat)
    date = futureDate(datetime.date(), 90)
    return date.strftime('%Y-%m-%d'), datetime.strftime('%H:%M')


def getData(event):
    if ("jazz" in event.text.lower() or "lindy hop" in event.text.lower()):
        time_element = re.search(r'\d\d:\d\d( tot \d\d:\d\d)?', event.text)
        if not time_element:
             return
        time_element = time_element[0]
        date_string, title = event.text.split(time_element)
        date_time_string = ' '.join(date_string.split()[:3]) + ' ' + time_element.split()[0]
        date, time = formatDate(date_time_string)
        return {
            'date': date,
            'time': time,
            'title': title,
            'venue': "Breugem Meeting Point",
            'price': "gratis",
            'site': "https://www.breugemmeetingpoint.nl/agenda",
            'address': "Nieuwe Hemweg 2, 1013 BG Amsterdam"
        }

def getEventList():
    url = 'https://www.breugemmeetingpoint.nl/agenda'
    return makeSoup(url).select('h3')

def bot():
    return map(getData, getEventList())
