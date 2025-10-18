from src.tools.scraper_tools import myStrptime
from src.tools.scraper_tools import makeSoup

def formatDate(dateString):
    dateFormat = '%A %d-%m-%Y, %H.%M uur'
    date = myStrptime(dateString, dateFormat)
    return date.strftime('%Y-%m-%d'), date.strftime('%H:%M')

def getData(event):
    date, time = formatDate(event.select_one('font[size="4"]').contents[1])
    return {
        'date': date,
        'time': time,
        'title': event.select_one('font[size="4"] p font[size="5"]').contents[0].text,
        'venue': "Einde van de Wereld",
        'price': "",
        'site': "https://www.eindevandewereld.nl/agenda1.php",
        'address': "Javakade 61, 1019 BK Amsterdam"
    }

def getEventList():
    url = 'https://www.eindevandewereld.nl/agenda1.php'
    events = makeSoup(url).select('table')[-1].select('tr td:first-child')
    return events

def bot():
    return map(getData, getEventList())
    # return (gig for event in getEventList() for gig in getData(event))
