from src.tools.scraper_tools import myStrptime, futureDate, makeSeleniumSoup

CALENDARS = ["jazzAmsterdam", "alternativeAmsterdam"]

def formatDate(dateString):
    dateFormat = '%a, %d %b %Y'
    dateString = dateString.split("-")[0].strip() + " 2020"
    date = futureDate(myStrptime(dateString, dateFormat).date())
    return date.strftime('%Y-%m-%d')

def formatTime(time):
    return time.split("-")[0].strip().replace('.',':')

def formatPrice(price):
    price = price.strip()
    if len(price) > 7:
        return ""
    price = price.replace(".",",").lower()
    return price

def getData(event):
    eventTitle = event.select_one('.content h2').text
    eventData = {
        'date': formatDate(event.select_one('.post-meta .event-date-time .event-date-time-wrapper .event-date').text),
        'time': formatTime(event.select_one('.post-meta .event-date-time .event-date-time-wrapper .event-time').text),
        'title': eventTitle,
        'venue': "Volkshotel",
        'price': formatPrice(event.select_one('.post-meta .event-price strong').text),
        'site': event.get('href'),
        'address': "Wibautstraat 150, 1091 GR Amsterdam"
    }
    if 'jazz' in eventTitle.lower():
        yield {**eventData, 'calendar': 'jazzAmsterdam'}
    yield {**eventData, 'calendar': 'alternativeAmsterdam'}

def getEventList():
    url = 'https://www.volkshotel.nl/en/agenda/'
    scripts = [
        "document.querySelector('.see-more-container a').click();",
        "window.scrollTo(0, document.body.scrollHeight);",
        "window.scrollTo(0, document.body.scrollHeight);",
        "window.scrollTo(0, document.body.scrollHeight);",
        "window.scrollTo(0, document.body.scrollHeight);"
    ]
    events = makeSeleniumSoup(url, 1, scripts).select_one('.wrapper ul.posts').select('li > a.card')
    return events

def bot():
    return (gig for event in getEventList() for gig in getData(event))

