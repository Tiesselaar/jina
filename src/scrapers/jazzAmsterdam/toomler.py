from src.tools.scraper_tools import myStrptime
from src.tools.scraper_tools import makeSeleniumSoup
import datetime


def formatDate(dateString):
    dateFormat = '%A %B %d, %Y'
    date = myStrptime(dateString, dateFormat).date()
    return date.strftime('%Y-%m-%d')

def formatTime(times):
    for time_element in times:
        if "Start" in time_element.text:
            time_string = time_element.select_one('.hour').text
            time_format = '%I:%M %p'
            return datetime.datetime.strptime(time_string, time_format).time().isoformat()[0:5]

def getData(event):
    if event.select_one('h1.title').text == "Late Night Jazz":
        title = " - ".join(map(lambda x: x.text, event.select(':is(h1.title, h2.subtitle)')))
    # if "jazz" in title.lower():
        site = "https://app.guts.tickets" + event.get('href')
        subsoup = makeSeleniumSoup(site, 4, ["document.getElementsByClassName('info-tab')[0].click()"])
        return {
            'date': formatDate(subsoup.select_one('strong.date').text),
            'time': formatTime(subsoup.select('.event-time-item > .hour-label')),
            'title': title,
            'venue': subsoup.select_one('h3.venue-name').text,
            'price': subsoup.select_one('.ticket-price > .price').text,
            'site': "https://www.comedytrain.nl/late-night-jazz/",
            'address': subsoup.select_one('p.venue-address').text
        }

def getEventList():
    url = 'https://app.guts.tickets/hq789i/'
    events = makeSeleniumSoup(url, 3).select('a.shop-item')
    return events

def bot():
    return map(getData, getEventList())
