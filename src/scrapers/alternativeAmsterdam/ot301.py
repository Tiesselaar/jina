from src.tools.scraper_tools import myStrptime
from src.tools.scraper_tools import makeSeleniumSoup, futureDate

# CALENDARS = ['theaterAmsterdam', 'classicalAmsterdam']

def formatDate(dateString):
    dateString += " 2024"
    dateFormat = '%A %d %B %Y'
    date = myStrptime(dateString, dateFormat).date()
    date = futureDate(date)
    return date.strftime('%Y-%m-%d')

def getData(event_date):
    event, date = event_date
    location, time, price = event.select_one('span.meta').text.split(' // ')
    return {
        'date': date,
        'time': time.strip().rjust(5, '0'),
        'title': location.strip() + ": " + event.select_one('span.title').text,
        'venue': "OT301",
        'price': price.strip().replace(' ', ''),
        'site': 'https://www.ot301.nl' + event.get('href'),
        'address': "Overtoom 301, 1054 HW Amsterdam"
    }

def getEventList():
    url = 'https://www.ot301.nl/agenda'
    event_or_dates = makeSeleniumSoup(url, waitFor='#agenda > div').select('#agenda :is(div.head, a.event-item)')
    running_date = ""
    events = []
    for event_or_date in event_or_dates:
        if "head" in event_or_date.get('class'):
            running_date = formatDate(event_or_date.text)
        else:
            events.append((event_or_date, running_date))
    return events

def bot():
    return map(getData, getEventList())
    # return (gig for event in getEventList() for gig in getData(event))
