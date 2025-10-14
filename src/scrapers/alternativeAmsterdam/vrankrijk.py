from src.tools.scraper_tools import myStrptime
from src.tools.scraper_tools import makeSoup, futureDate

# CALENDARS = ['theaterAmsterdam', 'classicalAmsterdam']

def formatDate(dateString):
    dateString += " 2024"
    dateFormat = '%A, %b %d %Y'
    date = myStrptime(dateString, dateFormat).date()
    date = futureDate(date)
    return date.strftime('%Y-%m-%d')

# def formatPrice(price):
#     # format price as '\u20ac12,50' (no space!)
#     price = price.replace(' ','')
#     return price

def getData(event):
    details = event.select_one('.vrankrijk-main-event-details').text.split('|')
    return {
        'date': formatDate(details[0].strip()),
        'time': details[1].split()[0].replace('.', ':'),
        'title': event.select_one('.vrankrijk-main-event-info h2 a').text.strip(),
        'venue': "Vrankrijk",
        'price': "",
        'site': event.select_one('.vrankrijk-main-event-info h2 a').get('href'),
        'address': "Spuistraat 216, 1012 VT Amsterdam"
    }

def getEventList():
    url = 'https://vrankrijk.org/events/'
    events = makeSoup(url).select('#em-events-list-1 div.vrankrijk-main-events')
    return events

def bot():
    return map(getData, getEventList())
    # return (gig for event in getEventList() for gig in getData(event))
