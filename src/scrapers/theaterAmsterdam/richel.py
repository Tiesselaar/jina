from src.tools.scraper_tools import myStrptime
from src.tools.scraper_tools import makeSoup, makeSeleniumSoup, futureDate
import re

CALENDARS = ['theaterAmsterdam', 'jazzAmsterdam']

DATE_SELECTOR = ' > '.join([
    '.elementor-hidden-mobile',
    '.e-con-inner',
    '.elementor-element',
    '.elementor-widget-container',
    '.jet-listing',
    '.jet-listing-dynamic-field__inline-wrap',
    'div.jet-listing-dynamic-field__content'
])

def formatDateTime(dateString):
    print(dateString)
    dateFormat = '%d-%m-%Y - %H:%M'
    date = myStrptime(dateString, dateFormat)
    return date.strftime('%Y-%m-%d'), date.strftime('%H:%M')

def formatDate(dateString):
    dateString += " 2024"
    dateFormat = '%A %d %B %Y'
    date = myStrptime(dateString, dateFormat).date()
    date = futureDate(date)
    return date.strftime('%Y-%m-%d')

def makeFilter(dateFilter):
    start = formatDate(dateFilter[-1].text)
    end = formatDate(dateFilter[0].text)
    return start, end

def formatPrice(info, site):
    price_string = info[-1].text
    if "Reserveren":
        return ""
    price_string = "".join(price_string.split()[:2])
    if not re.match(r'€\d+\.\d\d', price_string):
        raise Exception("funny price: " + price_string)
    return "".join(price_string.replace('.00', ''))

def getData(event):
    site = event.select_one('a.jet-engine-listing-overlay-link').get('href')
    print(site)
    subsoup = makeSoup(site)
    description = subsoup.select_one('[data-elementor-type="wp-post"]')
    try:
        dates = [date for date in subsoup.select_one('h5.elementor-heading-title').contents if isinstance(date, str)]
    except:
        print('no date box: ' + site)
        return
    if len(dates) == 0:
        print('no dates')
    dateStart, dateEnd = makeFilter(event.select(DATE_SELECTOR))
    for date in dates:
        try:
            date, time = formatDateTime(date)
        except:
            print('not a date: ' + date)
            continue
        if dateStart <= date <= dateEnd:
            event_data =  {
                'date': date,
                'time': time,
                'title': event.select_one('h2.jet-listing-dynamic-field__content').text,
                'venue': "Theater De Richel",
                'price': formatPrice(subsoup.select('h5.elementor-heading-title'), site),
                'site': site,
                'address': "Nieuwezijds Voorburgwal 282, 1012 RT Amsterdam"
            }
            yield {**event_data, 'calendar': 'theaterAmsterdam'}
            if 'jazz' in description.text.lower():
                yield {**event_data, 'calendar': 'jazzAmsterdam'}

def getEventList():
    url = 'https://theaterderichel.nl/agenda/'
    scroll = 4 * ["window.scrollTo(0, document.body.scrollHeight);"]
    events = makeSeleniumSoup(url, 1, scroll).select('.elementor-widget-container .jet-listing-grid__item')
    return events

def bot():
    from concurrent.futures import ThreadPoolExecutor
    with ThreadPoolExecutor() as executor:
        gigs = [
            gig
            for gigs in executor.map(lambda event: list(getData(event)), getEventList())
            for gig in gigs
        ]
    if len(gigs) < 10:
        raise Exception('Fewer events than expected: ' + str(len(gigs)))
    return gigs
