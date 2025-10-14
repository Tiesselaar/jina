from src.tools.scraper_tools import myStrptime
from src.tools.scraper_tools import makeSoup, makeSeleniumSoup, futureDate
from datetime import datetime


def formatDate(headers):
    for header in headers:
        if header[:9] == "fc-dom-4-":
            return header[9:]
    raise Exception('date not in headers')

def getData(event):
    title = " ".join(event.select_one('.fc-list-event-title').text.split())
    if (
        "orkest" in title.lower() or
        "Gregoriaans" in title
    ):
        return {
            'date': formatDate(event.select_one('.fc-list-event-title').get('headers')),
            'time': event.select_one('td.fc-list-event-time').text.split()[0],
            'title': title,
            'venue': "Keizersgrachtkerk",
            'price': "",
            'site': "https://www.keizersgrachtkerk.nl" + event.select_one('td.fc-list-event-title > a').get('href'),
            'address': "Keizersgracht 566, 1017 EM Amsterdam"
        }

def getEventList():
    today = datetime.today()
    url = f'https://www.keizersgrachtkerk.nl/activiteiten/agenda#year={today.year}&month={today.month}&day={today.day}&view=list'
    events = makeSeleniumSoup(url, 1).select('.fc-list-table tbody tr.fc-event')
    return events

def bot():
    return map(getData, getEventList())
