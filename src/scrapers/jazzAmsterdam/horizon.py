from src.tools.scraper_tools import myStrptime
from src.tools.scraper_tools import makeSeleniumSoup, futureDate


def formatDate(dateString):
    dateString = dateString.strip()[:8]
    dateFormat = '%d-%m-%y'
    date = myStrptime(dateString, dateFormat).date()
    return date.strftime('%Y-%m-%d')

def formatTime(time):
    return time.split('|')[1].split()[0]

def getData(event):
    if "jazz" in event.text.lower():
        return {
            'date': formatDate(event.select_one('.wpem-event-details span.wpem-event-date-time-text').text),
            'time': formatTime(event.select_one('.wpem-event-details span.wpem-event-date-time-text').text),
            'title': event.select_one('.wpem-event-title > h3.wpem-heading-text').text,
            'venue': "Podium Horizon",
            'price': "", # formatPrice(subsoup.select_one('.prijs').text),
            'site': event.select_one('a.wpem-event-action-url').get('href'),
            'address': "Hembrugstraat 156, 1013 XC Amsterdam"
        }

def getEventList():
    url = 'https://www.podiumhorizon.nl/agenda/'
    clickButton = "document.getElementById('load_more_events').click()"
    events = makeSeleniumSoup(url, 1, 2*[clickButton]).select('.event_listings_main .wpem-event-box-col')
    return events

def bot():
    return map(getData, getEventList())
