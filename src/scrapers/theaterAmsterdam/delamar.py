from src.tools.scraper_tools import myStrptime
from src.tools.scraper_tools import makeSeleniumSoup, futureDate
import datetime

CALENDARS = ["theaterAmsterdam", "jazzAmsterdam"]

def formatDate(dateString):
    if dateString =="Vandaag":
        return datetime.date.today().isoformat()
    if dateString =="Morgen":
        return (datetime.date.today() + datetime.timedelta(days=1)).isoformat()
    dateString += " 2024"
    dateFormat = '%A %d %B %Y'
    date = myStrptime(dateString, dateFormat).date()
    date = futureDate(date)
    return date.strftime('%Y-%m-%d')

def formatTime(genre_blocks):
    for block in genre_blocks:
        if ' uur' in block.text:
            return block.text.strip(' uur')

def getData(event_date):
    event, date = event_date
    site = "https://delamar.nl" + event.select_one('a').get('href')
    test_text = event.text.lower()
    event_data =  {
        'date': date,
        'time': formatTime(event.select('.genre')),
        'title': event.select_one('.tile__text > h3 > span').text.strip(),
        'venue': "Café DeLaMar" if "Café DeLaMar" in event.text else "DeLaMar Theater",
        'price': "",
        'site': site,
        'address': "Marnixstraat 402, Amsterdam"
    }
    if 'jazz' in test_text:
        yield {**event_data, 'calendar': 'jazzAmsterdam'}
    yield {**event_data, 'calendar': 'theaterAmsterdam'}

def get_date(dates_events):
    for event_or_date in dates_events:
        if event_or_date.name == "span":
            date = formatDate(event_or_date.text)
        else:
            yield [event_or_date, date]


def getEventList():
    url = 'https://delamar.nl/agenda/'
    soup = makeSeleniumSoup(url, 6, ["document.querySelector('button.button--more').click()"])
    dates_events = soup.select('.productions__tiles :is(.productions__day > span , .tile.js-tile)')
    if len(dates_events) < 10:
        raise Exception('Fewer events than expected')
    return get_date(dates_events)

def bot():
    return (gig for event in getEventList() for gig in getData(event))
