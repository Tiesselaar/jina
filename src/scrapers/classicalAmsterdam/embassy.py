from src.tools.scraper_tools import myStrptime
from src.tools.scraper_tools import makeSeleniumSoup, futureDate
import re

def formatDate(paragraphs):
    dateString = [x for x in paragraphs if "Datum: " in x][0]
    # dateString += " 2024"
    dateFormat = 'Datum: %d %B %Y'
    date = myStrptime(dateString, dateFormat).date()
    # date = futureDate(date)
    return date.strftime('%Y-%m-%d')

def formatTime(paragraphs):
    time = [x for x in paragraphs if "Tijd: " in x][0]
    return time.strip("Tijd: ")[:5].replace('.',':')

def formatPrice(paragraphs):
    price = [x for x in paragraphs if "Entree: " in x][0]        
    price = re.search(r'€ ?\d+(,\d\d?)?', price)[0]
    return price.replace(' ','')

def getData(event):
    paragraphs = [x.text for x in event.select('p')]
    if "Lunchconcert" in event.text:
        return {
            'date': formatDate(paragraphs),
            'time': formatTime(paragraphs),
            'title': event.select_one('h5').text + " - " + event.select_one('h5 + div p').text,
            'venue': "Embassy of the Free Mind",
            'price': formatPrice(paragraphs),
            'site': "https://tickets.embassyofthefreemind.com" + event.select_one('a').get('href'),
            'address': "Keizersgracht 123, 1015 CJ Amsterdam"
        }

def getEventList():
    url = 'https://tickets.embassyofthefreemind.com/category/381/culturele--kinderen-evenementen'
    events = makeSeleniumSoup(url, 5).select('div[slug="culturele--kinderen-evenementen"] .storefront-categoryless .storefront-column .card-inner')
    return events

def bot():
    return map(getData, getEventList())
