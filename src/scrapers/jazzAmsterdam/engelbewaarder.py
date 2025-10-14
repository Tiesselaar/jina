from src.tools.scraper_tools import myStrptime, makeSoup, makeSeleniumSoup, futureDate

def formatDate(day, month):
    dateString = ' '.join([day, month, "2024"])
    dateFormat = '%d %B %Y'
    date = myStrptime(dateString, dateFormat).date()
    date = futureDate(date, 35)
    return date.strftime('%Y-%m-%d')

def getData(event_month):
    event, month = event_month
    day = event.select_one('.date').text.strip()
    month = month.select_one('mat-panel-title').text.strip()
    artist = event.select_one('li.ng-star-inserted').text.strip()
    if 'Cancelled' in artist:
        return
    if 'no jazz' in month:
        return
    if artist == "tba":
        artist = ""
    feature = artist and " feat. " + artist

    return {
        'date': formatDate(day, month),
        'time': '16:30',
        'title': 'Jazz op zondag' + feature,
        'venue': "Café de Engelbewaarder",
        'price': "gratis",
        'site': "https://www.jazzengel.nl",
        'address': 'Kloveniersburgwal 59HS, 1011 JZ Amsterdam'
    }

def getEventList():
    url = 'https://www.jazzengel.nl'
    script = """document.querySelector('a[routerlink="program"]').click()"""
    soup = makeSeleniumSoup(url, 2, [script])
    months = soup.select('mat-expansion-panel.month')
    events = [[event, month] for month in months for event in month.select('mat-expansion-panel.date')][:30]
    if len(events) < 5:
        raise Exception('Fewer events than expected!')
    return events

def bot():
    return map(getData, getEventList())

