from src.tools.scraper_tools import myStrptime
from src.tools.scraper_tools import makeSoup, makeSeleniumSoup, futureDate
import re

def formatDate(dateString):
    dateString = dateString.replace('Wedesday', 'Wednesday').strip()
    dateFormat = '%A, %d %B, %Y - %H:%M'
    date = myStrptime(dateString, dateFormat).date()
    return date.strftime('%Y-%m-%d')

def formatPrice(description):
    price_search = re.search(r'€( ?)+\d+([,\.]\d\d?)?', description)
    if price_search:
        return price_search[0].replace(' ', '').replace(',','.')
    free_search = re.search(r'FREE entry', description)
    if free_search:
        return "free"
    return ""

def getData(event):
    site = event.select_one('p a').get('href')
    if not 'https' in site:
        site = "https://www.erc.amsterdam" + site
    subsoup = makeSoup(site)
    return {
        'date': formatDate(event.select_one('h4').text),
        'time': event.select_one('h4').text.split()[-1],
        'title': " - ".join(x.text for x in event.select(':is(h2, h3, h4)')[1:]),
        'venue': "English Reformed Church",
        'price': formatPrice(subsoup.select_one('article.eventitem').text),
        'site': site,
        'address': "Begijnhof 48, 1012 WV Amsterdam"
    }

def getEventList():
    url = 'https://www.erc.amsterdam/concerts'
    events = makeSeleniumSoup(url).select('.sqs-block .sqs-block-content .sqs-html-content')
    return [x for x in events if "20" in x.text]

def bot():
    return map(getData, getEventList())
