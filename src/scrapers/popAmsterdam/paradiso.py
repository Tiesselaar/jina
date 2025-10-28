from src.tools.scraper_tools import myStrptime, makeSoup, makeSeleniumSoup, futureDate
import re

CALENDARS = ['popAmsterdam', 'jazzAmsterdam']

def formatDate(date):
    # format date '31-1-2023'
    if not re.search(r'20\d\d', date):
        date += " 2020"
    dateFormat = '%A %d %B %Y'
    myDate = futureDate(myStrptime(date, dateFormat).date())
    return myDate.strftime('%Y-%m-%d')

def formatTime(time):
    voorprogramma = re.search(r"Voorprogramma: \d\d:\d\d", time)
    if voorprogramma:
        return voorprogramma[0][-5:]
    hoofdprogramma = re.search(r"Hoofdprogramma: \d\d:\d\d", time)
    if hoofdprogramma:
        return hoofdprogramma[0][-5:]
    time = re.search(r"\d\d:\d\d", time)[0]
    return time

def formatPrice(price):
    price = "".join(price.split())
    price = re.search(r'Ticket€\d*(,\d\d)?', price)[0]
    price = price.replace('Ticket','')
    return price

def formatAddress(maps_link):
    query = maps_link.split('query=')[1]
    return ",".join(query.split(',')[1:]).replace(', Noord, ', ', ').replace(', Centrum, ', ', ')

def getData(event):
    site = 'https://www.paradiso.nl' + event.get('href')
    print(site)
    subsoup = makeSoup(site)
    datePlaceTime = subsoup.select(".chakra-container > div > div > p.chakra-text")

    eventData = {
        'date': formatDate(datePlaceTime[0].text),
        'time': formatTime(datePlaceTime[2].text),
        'title': event.select_one('h2').text.strip(),
        'venue': datePlaceTime[1].text.replace("In ", "").split("-")[0].strip(),
        'price': "",
        'site': site,
        'address': formatAddress(subsoup.select_one('a[href^="https://www.google.com/maps/"]').get('href'))
    }
    try:
        eventData['price'] = formatPrice(subsoup.select_one('a[href^="https://"].chakra-button').text)
    except Exception as e:
        print("No price")
        eventData['price'] = ""
    if ("jazz" in event.text.lower() or
        "hi-stakes" in event.text.lower()):
        yield {**eventData, 'calendar': 'jazzAmsterdam'}
    yield {**eventData, 'calendar': 'popAmsterdam'}

def getEventList():
    venue_name = 'paradiso'
    url = 'https://www.paradiso.nl'
    script = ("window.scrollTo(0, document.body.scrollHeight);" for i in range(8))
    events = makeSeleniumSoup(url, 1, script).select('a[href*="/program"]:not(.chakra-link)')
    return events


def bot():
    from concurrent.futures import ThreadPoolExecutor
    with ThreadPoolExecutor() as executor:
        return (
            gig
            for gigs in executor.map(lambda event: list(getData(event)), getEventList())
            for gig in gigs
        )