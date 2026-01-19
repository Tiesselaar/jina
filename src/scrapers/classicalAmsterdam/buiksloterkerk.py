from src.tools.scraper_tools import myStrptime
from src.tools.scraper_tools import makeSoup, futureDate
import re

def formatDate(dateString):
    dateFormat = '%d %B %Y om %H:%M'
    date = myStrptime(dateString, dateFormat)
    return date.strftime('%Y-%m-%d'), date.strftime('%H:%M')

def formatPrice(description):
    if "evenement is gratis" in description:
        return "free"
    description = " ".join(description.split())
    price = re.search(r'€ ?\d+([,.]\d\d?)? \( normaal', description)[0]
    return price.strip("( normaal)").replace(',','.').replace(' ','')

def getData(event):
    date, time = formatDate(event.select_one('.card-body h6.text-secondary').text.strip())
    return {
        'date': date,
        'time': time,
        'title': event.select_one('.card-body .card-title').text.strip(),
        'venue': "Buiksloterkerk",
        'price': formatPrice(event.text),
        'site': event.select_one('a.event-card').get('href'),
        'address': "Buiksloterkerkpad 10, 1034 VZ Amsterdam"
    }

def getEventList():
    url = 'https://buiksloterkerk.nl/agenda/'
    events = makeSoup(url).select('.event-list .card')
    return events

def bot():
    return map(getData, getEventList())
