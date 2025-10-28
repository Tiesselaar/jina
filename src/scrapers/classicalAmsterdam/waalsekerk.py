from src.tools.scraper_tools import myStrptime
from src.tools.scraper_tools import makeSoup
import re

CALENDARS = ['classicalAmsterdam', 'jazzAmsterdam']

def formatDate(dateString):
    dateString = dateString.split('om')[0]
    dateString = dateString.split('van')[0]
    dateString = dateString.strip().replace(".","")
    ad_hoc = dateString.split(' t/m ')
    if len(ad_hoc) == 2 and ad_hoc[0] == ad_hoc[1]:
        dateString = ad_hoc[0]

    dateFormat = '%a %d %b %Y'
    date = myStrptime(dateString, dateFormat).date()
    return date.strftime('%Y-%m-%d')

def formatTime(time):
    time = time.split('om')[-1]
    time = time.split('van')[-1]
    time = time.split('-')[0]
    return time.strip()

def formatPrice(description):
    price = re.search(r'€ ?\d+([,.]\d\d)?', description)
    if price:
        return price[0].replace(' ', '')
    elif "gratis" in description.lower():
        return "free"
    else:
        return ""

def getData(event):
    site = event.select_one('a').get('href')
    print(site)
    subsoup = makeSoup(site)
    event_data = {
        'date': formatDate(event.select_one('h3 + p + p').text),
        'time': formatTime(event.select_one('h3 + p + p').text),
        'title': (event.select_one('h3').text + " - " + event.select_one('h3 + p').text).strip(" -"),
        'venue': "De Waalse Kerk",
        'price': formatPrice(subsoup.select_one('.container > .type-detail').text),
        'site': site,
        'address': "Walenpleintje 157-159, 1012 JZ Amsterdam"
    }
    yield {**event_data, 'calendar': 'classicalAmsterdam'}
    if "jazz" in " ".join(map(lambda x: x.text, subsoup.select('h1 ~ p'))).lower():
        yield {**event_data, 'calendar': 'jazzAmsterdam'}


def getEventList():
    url = 'https://dewaalsekerk.nl/agenda#Muziek'
    events = makeSoup(url).select('main .container .group')
    return events

def bot():
    from concurrent.futures import ThreadPoolExecutor
    with ThreadPoolExecutor() as executor:
        return (
            gig
            for gigs in executor.map(lambda event: list(getData(event)), getEventList())
            for gig in gigs
        )