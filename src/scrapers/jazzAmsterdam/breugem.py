from src.tools.scraper_tools import myStrptime
from src.tools.scraper_tools import makeSoup, futureDate


def formatDate(dateString):
    dateString += " 2024"
    dateFormat = '%A %d %B %H:%M %Y'
    datetime = myStrptime(dateString, dateFormat)
    date = futureDate(datetime.date(), 60)
    return date.strftime('%Y-%m-%d'), datetime.strftime('%H:%M') 


def getData(event):
    if ("jazz" in event.text.lower() or "lindy hop" in event.text.lower()):
        date, time = formatDate(" ".join(event.text.replace("-", "").split()[0:4]))
        return {
            'date': date,
            'time': time,
            'title': "-".join(event.text.split('-')[2:]).strip(),
            'venue': "Breugem Meeting Point",
            'price': "gratis",
            'site': "https://www.breugemmeetingpoint.nl/agenda",
            'address': "Nieuwe Hemweg 2, 1013 BG Amsterdam"
        }

def getEventList():
    url = 'https://www.breugemmeetingpoint.nl/agenda'
    return makeSoup(url).select('h3.jw-heading-70 > span')

def bot():
    return map(getData, getEventList())
