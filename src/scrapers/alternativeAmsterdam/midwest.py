from src.tools.scraper_tools import myStrptime
from src.tools.scraper_tools import makeSoup
import datetime
import re

CALENDARS = ["alternativeAmsterdam", "jazzAmsterdam", "popAmsterdam", "theaterAmsterdam"]

def formatDate(dateString):
    dateFormat = '%d|%m|%Y'
    date = myStrptime(dateString, dateFormat).date()
    return date.strftime('%Y-%m-%d')

def formatTime(description):
    try:
        time = re.search(r"(\d\d[:.]\d\d)[ .u]", description).group(1).replace(".",":")
        return time
    except:
        pass
    try:
        time = re.search(r"\d\d-\d\du", description)[0][:2] + ":00"
        return time
    except:
        pass
    try:
        time = re.search(r" \d\du ", description)[0][1:3] + ":00"
        return time
    except:
        pass


def formatPrice(description):
    try:
        return re.search(r"€ ?\d*([.,]\d\d?)?", description)[0].replace(".",",").replace(" ","")
    except:
        return ""

def getCalendar(description):
    if "jazz" in description.lower():
        yield "jazzAmsterdam"
    if "hip hop" in description.lower() or \
       "live optreden" in description.lower() or \
       "concert" in description.lower()  or \
       "muziek" in description.lower() or \
       "songwriter" in description.lower():
        yield "popAmsterdam"
    if "theater" in description.lower():
        yield "theaterAmsterdam"
    yield "alternativeAmsterdam"

def getData(event):
    site = event.select_one('a.agenda-overview_link').get('href')
    description = makeSoup(site).select_one('article').text
    time = formatTime(description)
    if not time:
        print("No time")
        return
    eventData = {
        'date': formatDate(event.select_one('time.agenda-overview_date').text),
        'time': time,
        'title': event.select_one('a.agenda-overview_link').text,
        'venue': "Midwest",
        'price': formatPrice(description),
        'site': site,
        'address': "Cabralstraat 1, 1057 CD Amsterdam"
    }
    for calendar in getCalendar(description):
        yield {**eventData, 'calendar': calendar}

def getEventList():
    url = 'https://www.inmidwest.nl/agenda-overzicht/?month='
    def format_month(month):
        return month.isoformat().replace('-', '')[:6]
    months = [
        format_month(
            datetime.date.today() -
            datetime.timedelta(days=datetime.date.today().day - 1 - 31 * i)
        )
        for i in range(3)
    ]
    css_selector = 'section.agenda-overview > .container > .agenda-overview-month > .grid-item'
    events = sum(list(makeSoup(url + month).select(css_selector) for month in months), [])
    return events

def bot():
    return (gig for event in getEventList() for gig in getData(event))
