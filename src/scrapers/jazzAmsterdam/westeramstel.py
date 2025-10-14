from src.tools.scraper_tools import myStrptime, futureDate, makeSoup

def formatDate(dateString):
    dateString = " ".join(dateString.split()) + " 2024"
    dateFormat = '%d %B %A %Y'
    date = futureDate(myStrptime(dateString, dateFormat).date())
    return date.strftime('%Y-%m-%d')

def getData(event):
    eventLink = event.select_one('h4.mec-event-title a.mec-color-hover')
    if "jazz" in eventLink.text.lower():
        eventData = {
            'date': formatDate(event.select_one('.mec-event-date').text),
            'time': "15:00",
            'title': eventLink.text.replace('Sasha Beets', 'Dasha Beets'),
            'venue': "Wester-Amstel",
            'price': "€15",
            'site': eventLink.get('href'),
            'address': "Amsteldijk Noord 55, 1183 TE Amstelveen"
        }
        return eventData

def getEventList():
    venue_name = 'westeramstel'
    URL = 'https://wester-amstel.nl/agenda/'
    events = makeSoup(URL).select('.mec-event-list-modern > article.mec-event-article')
    return events

def bot():
    return map(getData, getEventList())


