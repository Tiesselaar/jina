from src.tools.scraper_tools import myStrptime
from src.tools.scraper_tools import makeSeleniumSoup, futureDate

def formatDate(dateString):
    dateString += " 2024"
    dateString = dateString.replace(',','')
    dateFormat = '%A %b %d %H:%M %Y'
    date = myStrptime(dateString, dateFormat)
    time = date.strftime('%H:%M')
    date = futureDate(date.date())
    return date.strftime('%Y-%m-%d'), time


def getData(event):
    site = "https://contra.weticket.io/" + event.get('href')
    date, time = formatDate(event.select_one('span').text)
    return {
        'date': date,
        'time': time,
        'title': event.select_one('h5').text,
        'venue': "Contra",
        'price': "",
        'site': site,
        'address': "Oudezijds Achterburgwal 235, 1012DL Amsterdam"
    }

def getEventList():
    url = 'https://contra.weticket.io'
    events = makeSeleniumSoup(url).select('main > div > div > div > a')
    return events

def bot():
    return map(getData, getEventList())