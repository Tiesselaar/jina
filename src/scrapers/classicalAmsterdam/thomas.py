from src.tools.scraper_tools import myStrptime
from src.tools.scraper_tools import makeSoup, futureDate


def formatDate(dateString):
    # dateString += " 2024"
    dateFormat = '%d %b %Y'
    date = myStrptime(dateString, dateFormat).date()
    # date = futureDate(date)
    return date.strftime('%Y-%m-%d')

def formatPrice(description):
    if "je kunt gratis binnenlopen" in description:
        return "free"
    return ""

def getData(event):
    site = event.select_one('.mec-event-content h4.mec-event-title a').get('href')
    subsoup = makeSoup(site)
    description = subsoup.select_one('section#main-content').text
    if 'concert' in description:
        return {
            'date': formatDate(subsoup.select_one('.mec-single-event-date .mec-start-date-label').text),
            'time': subsoup.select_one('.mec-single-event-time .mec-events-abbr').text.split()[0],
            'title': event.select_one('.mec-event-content h4.mec-event-title a').text,
            'venue': "De Thomas",
            'price': formatPrice(description),
            'site': site,
            'address': "Prinses Irenestraat 36, 1077 WX Amsterdam"
        }

def getEventList():
    url = 'https://dethomas.nl/programma/'
    events = makeSoup(url).select('article.mec-event-article')
    return events

def bot():
    from concurrent.futures import ThreadPoolExecutor
    with ThreadPoolExecutor() as executor:
        results = list(executor.map(getData, getEventList()))
    return results
