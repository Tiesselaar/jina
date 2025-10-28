from src.tools.scraper_tools import myStrptime
from src.tools.scraper_tools import makeSoup, makeSeleniumSoup

CALENDARS = ['theaterAmsterdam', 'jazzAmsterdam']

def formatDate(dateString):
    dateString = dateString.split('-')[0].replace(".", "")
    dateFormat = '%a %d %b %Y'
    date = myStrptime(dateString, dateFormat).date()
    return date.strftime('%Y-%m-%d')

def formatTime(time):
    return time.split('-')[1].split()[0].replace(".",":")

def getData(event):
    site = 'https://griffioen.vu.nl' + event.get('onclick').split("'")[1]
    print(site)
    subsoup = makeSoup(site)
    description = "\n".join(map(lambda x: x.text, subsoup.select('.contentblock .textblock p')))
    # shop = makeSoup('https://griffioen.vu.nl' + subsoup.select_one('.conversion-order > a[data-hook^="order-link"]').get('href'))
    # print(site)
    eventData = {
        'date': formatDate(event.select_one('time').text),
        'time': formatTime(event.select_one('time').text),
        'title': event.select_one('strong').text.replace('\u00a0', ' '),
        'venue': "Theater de Griffioen",
        'price': "", # formatPrice(shop.select_one('span[data-hook="price"]').text),
        'site': site,
        'address': "De Boelelaan 1111, 1081 HV Amsterdam",
    }
    yield { **eventData, 'calendar': "theaterAmsterdam" }
    if 'jazz' in description:
        yield { **eventData, 'calendar': "jazzAmsterdam" }

def getEventList():    
    url = "https://griffioen.vu.nl/voorstellingen#page:"
    return [event for page in range(1,5) for event in makeSeleniumSoup(url + str(page)).select('.program-item')]

def bot():
    from concurrent.futures import ThreadPoolExecutor
    with ThreadPoolExecutor() as executor:
        return (
            gig
            for gigs in executor.map(lambda event: list(getData(event)), getEventList())
            for gig in gigs
        )