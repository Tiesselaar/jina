from src.tools.scraper_tools import myStrptime
from src.tools.scraper_tools import makeSeleniumSoup, futureDate
from datetime import datetime

def formatDate(dateString):
    weekday = ['ma','di','wo','do','vr','za','zo'][datetime.today().weekday()]
    dateString = " ".join(dateString.split()).lower().replace('vandaag', weekday)
    dateString += " 2024"
    dateFormat = '%a %d %b %Y'
    date = myStrptime(dateString, dateFormat).date()
    date = futureDate(date)
    return date.strftime('%Y-%m-%d')

# def formatTime(time):
#     # format time as '21:00'
#     return time

# def formatPrice(price):
#     # format price as '\u20ac12,50' (no space!)
#     price = price.replace(' ','')
#     return price

def getData(day_event):
    day, event = day_event
    time = event.select_one('.agendaItem__item-date').text.split()[0]
    if "afgelast" in time.lower():
        return
    return {
        'date': day,
        'time': time,
        'title': event.select_one('.agendaItem__item-title span').text,
        'venue': "ITA",
        'price': "",
        'site': event.get('href'),
        'address': "Leidseplein 26, 1017 PT Amsterdam"
    }

def getEventList():
    url = 'https://ita.nl/nl/agenda/'
    days = makeSeleniumSoup(url).select('.agenda__day-container')
    return ([
        formatDate(day.select_one('.agenda__day-title').text),
        event
    ] for day in days for event in day.select('.agenda__list-container a.agendaItem__item'))

def bot():
    return map(getData, getEventList())
