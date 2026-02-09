from src.tools.scraper_tools import myStrptime
from src.tools.scraper_tools import makeSoup, futureDate
import re

# CALENDARS = ['theaterAmsterdam', 'classicalAmsterdam']

def formatDate(dateString):
    dateString = dateString.replace('.','')
    week_day, day, month = dateString.split()
    dateString = " ".join([week_day, day, month[:3]]).replace(' maa', ' mrt')
    dateString += " 2024"
    dateFormat = '%a %d %b %Y'
    date = myStrptime(dateString, dateFormat).date()
    date = futureDate(date, 60)
    return date.strftime('%Y-%m-%d')

def getPrice(event):
    if "Free" in event.text:
        return "free"
    subsoup = makeSoup(event.select_one('a.elementor-button-link').get('href'))
    price_search = re.search(r"tickets \(standaard\): € \d+,(-|\d\d)", subsoup.text)
    if price_search:
        return "".join(price_search[0].split()[-2:]).replace(',','.').replace('.-','')
    return ""

def getData(event):
    date_time = event.select_one('div > div > div > div.elementor-widget-container > p')
    if not date_time:
        return
    date_time = date_time.text
    if "Schrijf u in voor het Marionetten Nieuws" in date_time or \
        "Mail ons dan: info@marionettentheater.nl" in date_time or \
        "en verder:  educatieve activiteiten" in date_time:
        return
    date = " ".join(date_time.split()[:3]).replace('.', '')
    time = date_time.split()[3].replace('.',':')
    if "Comedy" in time:
        return
    if time == "Concert:":
        return
    return {
        'date': formatDate(date),
        'time': time,
        'title': event.select_one('p a').text,
        'venue': "Amsterdams Marionetten Theater",
        'price': getPrice(event),
        'site': event.select_one('p a').get('href'),
        'address': "Nieuwe Jonkerstraat 8, 1011 CM Amsterdam"
    }

def getEventList():
    url = 'https://www.marionettentheater.nl/agenda/'
    events = makeSoup(url).select('.elementor-container .elementor-column section.elementor-section[data-element_type="section"]')
    return events

def bot():
    return map(getData, getEventList())
    # return (gig for event in getEventList() for gig in getData(event))
