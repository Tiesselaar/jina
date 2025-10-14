from src.tools.scraper_tools import myStrptime, makeSoup

def formatDateTime(dateString):
    dateString = " ".join(dateString.split()[0:4])
    dateFormat = '%d %b %Y, %H:%M'
    date_time = myStrptime(dateString, dateFormat)
    return date_time.strftime('%Y-%m-%d'), date_time.strftime('%H:%M'), 

def getData(event):
    if "jazz" in event.text.lower():
        date, time = formatDateTime(event.select_one('[data-hook="date"]').text)
        eventData = {
            'date': date,
            'time': time,
            'title': event.select_one('[data-hook="title"] a').text,
            'venue': "Tolhuis",
            'price': "",
            'site': event.select_one('[data-hook="title"] a').get('href'),
            'address': "Buiksloterweg 7, 1031 CC Amsterdam"
        }
        return eventData

def getEventList():
    venue_name = 'tolhuis'
    url = 'https://www.tolhuis.nl/agenda'
    return makeSoup(url).select_one('ul[data-hook="events-cards"]').select('li[data-hook="events-card"]')

def bot():
    return map(getData, getEventList())


