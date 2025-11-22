from src.tools.scraper_tools import myStrptime
from src.tools.scraper_tools import makeSoup, makeSeleniumSoup, futureDate

CALENDARS = ['alternativeAmsterdam', 'jazzAmsterdam']

def formatDate(dateString):
    dateString += " 2024"
    dateFormat = '%B %d %Y'
    date = myStrptime(dateString, dateFormat).date()
    date = futureDate(date)
    return date.strftime('%Y-%m-%d')

def getData(event):
    site = event.select_one('.w-grid-item-h a').get('href')
    subsoup = makeSoup(site)
    description = subsoup.select_one('section:has(h1.post_title) + section + div').text
    eventData = {
        'date': formatDate(subsoup.select_one('._agenda_short_date span').text),
        'time': subsoup.select_one('.agenda_time_start span').text,
        'title': subsoup.select_one('h1.post_title').text,
        'venue': "De Nieuwe Anita",
        'price': "",
        'site': site,
        'address': "Frederik Hendrikstraat 111, 1052 HN Amsterdam"
    }
    if not eventData['time']:
        return
    if 'jazz' in description.lower() or 'gumbo night' in event.text.lower():
        yield {**eventData, 'calendar': 'jazzAmsterdam'}
    yield {**eventData, 'calendar': 'alternativeAmsterdam'}

def getEventList():
    url = 'https://denieuweanita.nl'
    events = makeSeleniumSoup(url).select('#us_grid_2 .w-grid-list article.w-grid-item')
    return events

def bot():
    from concurrent.futures import ThreadPoolExecutor
    with ThreadPoolExecutor() as executor:
        gig_list = list((
            gig
            for gigs in executor.map(lambda event: list(getData(event)), getEventList())
            for gig in gigs
        ))
    if len(gig_list) < 10:
        raise Exception('Fewer events than expected!!')
    return gig_list