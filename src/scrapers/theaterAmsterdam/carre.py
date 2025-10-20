from src.tools.scraper_tools import myStrptime
from src.tools.scraper_tools import makeSeleniumSoup
import re

CALENDARS = ['theaterAmsterdam', 'jazzAmsterdam']


def formatDate(dateString, noday = False):
    dateFormat = '%a %d %b %Y'
    if noday:
        dateFormat = '%d %b %Y'
    date = myStrptime(dateString, dateFormat).date()
    return date.strftime('%Y-%m-%d')
  
def formatPrice(price):
    print(price)
    price = price.replace("Engelse Boventiteling, ", "")
    if price == "wachtlijst":
        return "s.o."
    if price == "":
        return price
    price = re.search(r"va € \d+,\d\d", price)
    if price:
        return price[0].replace("va ", "").replace(" ","")
    return ""

def getData(event, shift=0):
    if shift > 4:
        return
    site, title = event
    print("Scraping", site, title)
    subsoup = makeSeleniumSoup(
        site,
        scripts = shift * ["document.querySelector('.pp-calendar > header > span.next').click()"],
        waitFor = ':is(.pp-calendar, .section__body)',
    )
    show = {
        'title': title,
        'venue': "Carré",
        'site': site,
        'address': "Amstel 115-125, 1018 EM Amsterdam"
    }

    # Scenario 1: shows are in calandar view

    if subsoup.select_one('.pp-calendar'):
        month = subsoup.select_one('.pp-calendar > header > span.day__month_btn').text
        days = subsoup.select('.pp-calendar > div > span.day:not(.other-month) > div')
        for day in days:
            event_day = day.select_one('div').text
            times = day.select('.pill-container > a')
            for time in times:
                yield {
                    **show,
                    'date': formatDate(" ".join([event_day, month]), noday=True),
                    'time': time.text.strip(),
                    'price': formatPrice(time.get('title'))
                }
        if subsoup.select_one('.pp-calendar > header > span.next:not(.disabled)'):
            print("Shifting calendar view to next month")
            yield from getData(event, shift + 1)

    # Scenario 2: shows are in list view

    else:
        months = subsoup.select('.section__body .section__group')
        if not months:
            raise ValueError("No shows found for {}".format(site))
        for month in months:
            year = month.select_one('h3.section__group-title').text.split()[1]
            subevents = month.select('.table-data > .table__row')
            if not subevents:
                raise ValueError("No shows found for {}".format(site))
            for subevent in subevents:
                yield {
                    **show,
                    'date': formatDate(" ".join([subevent.select_one('.date').text, year])),
                    'time': subevent.select_one('.time').text.strip(),
                    'price': formatPrice(subevent.select_one('.price').text),
            }

def getEventList(url):
    events = makeSeleniumSoup(url, waitFor='section.section-events').select('section.section-events .news-excerpt')[:30]
    unique_events = {
        "https://carre.nl" + event.select_one('span > a').get('href'):
        event.select_one('.news__content > h4 > a').text
        for event in events
    }
    return [[link, unique_events[link]] for link in unique_events]

def bot():
    url = {'theaterAmsterdam': 'https://carre.nl/agenda',
           'jazzAmsterdam': 'https://carre.nl/agenda?q=jazz'}
    return (
        {**gig, 'calendar': calendar} for calendar in CALENDARS for event in getEventList(url[calendar]) for gig in getData(event))
