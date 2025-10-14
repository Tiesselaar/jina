from src.tools.scraper_tools import myStrptime
from src.tools.scraper_tools import makeSoup, futureDate
import re

def formatDate(dateString):
    dateFormat = '%d.%m.%Y'
    date = myStrptime(dateString, dateFormat)
    return date.strftime('%Y-%m-%d')

def price(text):
    price_search = re.search(r"€\d\d?(.\d)?\d?", text)
    if price_search:
        return price_search[0].replace('.',',').replace(',00','')
    return ""


def getData(event):
    title_element = event.select_one('.post-header-title')
    if 'jazz' in title_element.text.lower():
        site = "https://kalemegdan.nl" + title_element.select_one('a').get('href')
        subsoup = makeSoup(site)
        
        eventData = {
            'date': formatDate(event.select_one('.post-info-date').text),
            'time': subsoup.select_one('.date-display-single').text.split(' - ')[1],
            'title': title_element.text.strip(),
            'venue': "Kalemegdan",
            'price': price(subsoup.text),
            'site': site,
            'address': "Tweede van Swindenstraat 94, 1093 VX Amsterdam"
        }
        return eventData

def getEventList():
    url = 'https://kalemegdan.nl/evenement'
    events = makeSoup(url).select('.elementor-widget-container > .blog-post-content-wrapper .post')[::-1]
    url = 'https://kalemegdan.nl/evenement?page=1'
    events2 = makeSoup(url).select('.elementor-widget-container > .blog-post-content-wrapper .post')[::-1]
    url = 'https://kalemegdan.nl/evenement?page=2'
    events3 = makeSoup(url).select('.elementor-widget-container > .blog-post-content-wrapper .post')[::-1]
    return events + events2 + events3

def bot():
    return map(getData, getEventList())