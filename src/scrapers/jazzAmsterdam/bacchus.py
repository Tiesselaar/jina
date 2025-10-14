from src.tools.scraper_tools import myStrptime
from src.tools.scraper_tools import makeSoup
import re

def formatDate(dateString):
    dateFormat = '%A %d %B %Y'
    date = myStrptime(dateString.split(' - ')[0], dateFormat)
    return date.strftime('%Y-%m-%d')

def getData(event):
    if "jazz" in event.text.lower():
        site = "https://www.cafebacchus.info/paginas/" + event.select_one('a').get('href')
        subsoup = makeSoup(site)
        return {
            'date': formatDate(event.select_one('td.plat').text),
            'time': re.search(r"begint om \d\d:\d\d", subsoup.text)[0][-5:],
            'title': event.select_one('span.tussenkop').text,
            'venue': "Cultureel Café Bacchus (Aalsmeer)",
            'price': "",
            'site': site,
            'address': "Gerberastraat 4, 1431 SG Aalsmeer"
        }

def getEventList():
    url = 'https://www.cafebacchus.info/paginas/programma.php'
    events = makeSoup(url).select('table table table table')
    return events

def bot():
    return map(getData, getEventList())
