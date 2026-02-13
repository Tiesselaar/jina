from src.tools.scraper_tools import myStrptime, futureDate, makeSoup
import re

def formatDate(date):
    dateFormat = '%A %d %B %Y'
    date += " 2020"
    date = futureDate(myStrptime(date, dateFormat).date(), 30)
    return date.strftime('%Y-%m-%d')

def formatTime(time):
    time = time.split()[0]
    return time

def formatPrice(price):
    match = re.search(r"€\d+(,(\d\d|-))?", price)
    return match[0].replace(",-", "") if match else ""

def getData(event):
    if "Jazz" in event.text:
        site = event.select_one('.programma-item-title-figure a').get('href')
        # subSoup = makeSeleniumSoup(site,2)
        return {
            'date': formatDate(event.select_one('.programma-item-inner .programma-item-datum-tijd p.programma-item-datum').text),
            'time': formatTime(event.select_one('.programma-item-inner .programma-item-datum-tijd p.programma-item-tijd').text),
            'title': event.select_one('.programma-item-title-figure a div h3 span').text,
            'venue': "Sociëteit de Kring",
            # 'price': formatPrice(subSoup.select_one('#site-content').text),
            'price': "",
            'site': site,
            'address': 'Kleine-Gartmanplantsoen 7-9, 1017 RP Amsterdam'
        }

def getEventList():
    url='https://kring.nl/programma/'
    events = makeSoup(url).select("div.programma-item-wrappers div.programma-item")
    if len(events) < 5:
        raise Exception("Too few events")
    return events

def bot():
    l = list(map(getData, getEventList()))
    if len(l) < 5:
        raise Exception("Too few events")
    return l


