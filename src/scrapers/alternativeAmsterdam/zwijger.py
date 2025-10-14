from src.tools.scraper_tools import myStrptime
from src.tools.scraper_tools import makeSoup, futureDate
import datetime

def formatDate(dateString):
    if dateString == "Morgen":
        date = datetime.date.today() + datetime.timedelta(days=1)
    else:
        dateString += " 2024"
        dateFormat = '%a %d %b %Y'
        date = myStrptime(dateString, dateFormat).date()
        date = futureDate(date)
    return date.strftime('%Y-%m-%d')

def formatPrice(price):
    if "gratis" in price.lower():
        return "free"
    price = price.replace(' ','')
    return price

def formatLocation(location, event, site):
    if any([
        "grote zaal pdz" in location,
        "studio pdz" in location,
        "ijzaal pdz" in location,
        "pakhuis de zwijger" in location,
    ]):
        return "Pakhuis de Zwijger", "Piet Heinkade 179, 1019 HC Amsterdam"
    if "op het Marineterrein" in event.text or "marineterrein" in location:
        return "Marineterrein", "Kattenburgerstraat 5, 1018 JA Amsterdam"
    if "at pakhuis de zwijger" in makeSoup(site).select_one('.page-main').text.lower():
        return "Pakhuis de Zwijger", "Piet Heinkade 179, 1019 HC Amsterdam"
    return "Pakhuis de Zwijger", "Piet Heinkade 179, 1019 HC Amsterdam"


def getData(event):
    site = "https://dezwijger.nl" + event.select_one('a.program-link').get('href')
    venue, address = formatLocation(event.select_one('.meta .location').text.lower(), event, site)
    return {
        'date': formatDate(event.select_one('.meta .date-time').text.split(',')[0]),
        'time': event.select_one('.meta .date-time').text.split(',')[1].strip().replace('.', ':'),
        'title': event.select_one('.details .title').text,
        'venue': venue,
        'price': formatPrice(event.select_one('.meta .entrance').text),
        'site': site,
        'address': address
    }

def getEventList():
    url = 'https://dezwijger.nl/agenda'
    events = makeSoup(url).select('.section.programs > .container > div.row:not(.container-title)')
    return events

def bot():
    return map(getData, getEventList())
