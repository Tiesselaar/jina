import datetime
import re
from src.tools.scraper_tools import makeSoup

CALENDARS = ["alternativeAmsterdam", "jazzAmsterdam"]

def formatDate(dateString):
    dateTuple = list(map(int,dateString.split('.')))
    dateTuple.reverse()
    dateTuple[0] = dateTuple[0] + 2000
    date = datetime.date(*dateTuple)
    return date.strftime('%Y-%m-%d')

def formatTime(agendaContent):
    timeSearch = re.search(r"\d\d?h(\d\d)?", agendaContent)
    if not timeSearch:
        return
    timeString = timeSearch[0]
    if len(timeString) < 4:
        timeString += "00"
    timeString = timeString.replace('h', ':')
    if not re.search(r'\d?\d:\d\d', timeString):
        raise Exception('Bad time')
    return timeString

def formatPrice(info):
    if re.search(r'Free entrance', info):
        return 'gratis'
    priceString = re.search(r'\d+([.,]\d\d?)?(€| euro)', info)
    if priceString:
        return '€' + priceString[0].replace('.',',').replace('€','').replace(' euro','')
    return ""

def getData(event):
    site = "https://www.treehousendsm.com" + event.select_one('a[href^="/agenda/"]').get('href')
    subsoup = makeSoup(site)
    time = formatTime(subsoup.select_one('.agenda_content p').text)
    if not time:
        return
    eventData = {
        'date': formatDate(event.select_one('.number_date').text),
        'time': time,
        'title': event.select_one('.title_card').text.title(),
        'venue': "Treehouse NDSM",
        'price': formatPrice(subsoup.select_one('.agenda_content p').text),
        'site': site,
        'address': "T.T. Neveritaweg 55-57, 1033 WB Amsterdam"
    }
    if "jazz" in subsoup.select_one('.agenda_content').text.lower():
        yield {**eventData, 'calendar': 'jazzAmsterdam'}
    yield {**eventData, 'calendar': 'alternativeAmsterdam'}

def getEventList():
    url = 'https://www.treehousendsm.com/pages/agenda-tiles'
    events = makeSoup(url).select('.agenda_wrapper > .post_wrapper > div[role="list"] > div[role="listitem"]')
    return events

def bot():
    from concurrent.futures import ThreadPoolExecutor
    with ThreadPoolExecutor() as executor:
        return (
            gig
            for gigs in executor.map(lambda event: list(getData(event)), getEventList())
            for gig in gigs
        )