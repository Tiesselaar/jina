from src.tools.scraper_tools import makeSoup
import urllib

def getData(event):
    title = event.select_one('.simcal-event-title').text
    if any(
        keyword in title.lower() for keyword in ["klassiek", "flamenco", "zuid-amerikaans"]
    ):
        return {
            'date': event.select_one('.simcal-event-start').get('content')[:10],
            'time': event.select_one('.simcal-event-start').get('content')[11:16],
            'title': title.replace('Concert: ', ''),
            'venue': "De Roode Remise",
            'price': "free",
            'site': "https://rooderemise.nl/activiteiten/#:~:text=" + urllib.parse.quote(title),
            'address': "Haarlemmerplein 11, 1013 HP Amsterdam"
        }

def getEventList():
    url = 'https://rooderemise.nl/activiteiten/'
    events = makeSoup(url).select('.simcal-calendar .simcal-calendar-list li.simcal-event')
    return events

def bot():
    return map(getData, getEventList())