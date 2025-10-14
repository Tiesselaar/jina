from src.tools.scraper_tools import myStrptime, futureDate, makeSoup, makeSeleniumSoup

CALENDARS = ['theaterAmsterdam', 'jazzAmsterdam', 'classicalAmsterdam']

def formatDate(date):
    date += " 2024"
    dateFormat = '%a %d %b %Y'
    myDate = futureDate(myStrptime(date, dateFormat).date())
    return myDate.strftime('%Y-%m-%d')

def formatPrice(price):
    if not price:
        return ""
    return "".join(price.text.split()).replace(',','.').replace('.00','').split('-')[-1]

def formatLocation(venue):
    if venue in ["Foyer", "Theaterzaal", "Studiozaal 1", "Studiozaal 2", "Buiten"]:
        return "Bijlmer Parktheater", "Anton de Komplein 240, 1102 DR Amsterdam"
    elif "SHEBANG" in venue:
        return "SHEBANG", "Hettenheuvelweg 8, 1101 BN Amsterdam"
    else:
        raise Exception('Unknown venue: ' + venue)
    
def getData(event):
    site = "https://www.bijlmerparktheater.nl" + event.select_one('a.desc').get('href')
    venueTag = event.select_one('.venue').text.strip()
    venue, address = formatLocation(venueTag)
    event_data = {
        'date': formatDate(event.select_one('.dateTimeInner .datetime .date .start').text.strip()),
        'time': event.select_one('.dateTimeInner .datetime .time .start').text.strip(),
        'title': " - ".join([*map(lambda tag: tag.text, event.select('a.desc :is(.title, .subtitle)'))][::-1]),
        'venue': venue,
        'price': formatPrice(event.select_one('.price')),
        'site': site,
        'address': address
    }
    ## A bit more complete (maybe even picks up too much), million times slower:
    # subsoup = makeSeleniumSoup(site)
    # if "jazz" in subsoup.select_one('.container .desc1').text.lower() or "jazz" in event.text.lower():
    #     yield {**event_data, 'calendar': 'jazzAmsterdam'}
    # if "klassiek" in subsoup.select_one('.container .desc1').text.lower() or "klassiek" in event.text.lower():
    #     yield {**event_data, 'calendar': 'classicalAmsterdam'}

    if "jazz" in event.text.lower():
        yield {**event_data, 'calendar': 'jazzAmsterdam'}
    if "klassiek" in event.text.lower():
        yield {**event_data, 'calendar': 'classicalAmsterdam'}
    yield {**event_data, 'calendar': 'theaterAmsterdam'}

def getEventList():
    url = 'https://www.bijlmerparktheater.nl/agenda?list_type=events&max=36&page='
    return [event for page in range(1,3) for event in makeSeleniumSoup(url + str(page)).select('ul.listItems li.eventCard')]

def bot():
    return (gig for event in getEventList() for gig in getData(event))
