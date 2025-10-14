from src.tools.scraper_tools import myStrptime
from src.tools.scraper_tools import makeSoup, futureDate


def formatDate(dateString):
    dateString += "/2025"
    dateFormat = '%d/%m/%Y'
    date = myStrptime(dateString, dateFormat).date()
    # date = futureDate(date)
    return date.strftime('%Y-%m-%d')

def getData(event):
    return {
        'date': formatDate(event.select_one('td').text.strip()),
        'time': event.select('td')[1].text.split("-")[0].strip().replace(".",":"),
        'title': event.select('td')[2].text.strip(),
        'venue': event.select('td')[3].text.strip(),
        'price': "gratis",
        'site': "https://www.conservatoriumvanamsterdam.nl/agenda/eindexamens/",
        'address': "Oosterdokskade 151, 1011 DL Amsterdam"
    }

def getEventList():
    url = 'https://www.conservatoriumvanamsterdam.nl/agenda/eindexamens/jazz/'
    return makeSoup(url).select('#main-content table > tbody > tr')[1:]

def bot():
    return map(getData, getEventList())
