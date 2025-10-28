from src.tools.scraper_tools import myStrptime, makeSoup

CALENDARS = ["theaterAmsterdam", "jazzAmsterdam"]

def formatDate(date, year):
    date = date.replace('\u00a0',' ') + ' ' + year
    dateFormat = '%a %d %B %Y'
    try:
        my_date = myStrptime(date, dateFormat)
    except:
        my_date = myStrptime(date[0:-5], dateFormat)
    return my_date.strftime('%Y-%m-%d')

def formatTime(time):
    time = time.split('-')[0].replace('\u00a0','').replace('uur','').strip()
    return time

def formatPrice(price):
    if not price:
        return ""
    price = price.text.split('\u2013')[0]
    price = price.replace('kaarten','').replace(' ','').replace(',00','')
    return price

def getData(event):
    site = event.get('href')
    print(site)
    subsoup = makeSoup(site)
    if "Geannuleerd" in subsoup.select_one('.databox .datum-bestel').text:
        return
    info_div = event.select_one('.evenement-datumtijd-info > .evenement-datumtijd')
    times = info_div.select('.evenement-tijd h4')
    for time in times:
        event_year = event.get('href').split('?datum=')[1][0:4]
        event_data =  {
            'date': formatDate(info_div.select_one('h3').text, event_year),
            'time': formatTime(time.text),
            'title': event.select_one('.itemtext > h1').text,
            'venue': "Theater Mascini",
            'price': formatPrice(subsoup.select_one('.datum-bestel .prijzen-info .prijs')),
            'site': site,
            'address': 'Zeedijk 24a, 1012 AZ Amsterdam'
        }
        if "Jazz" in subsoup.select_one('.databox .itemtext').text:
            yield {**event_data, 'calendar': 'jazzAmsterdam'}
        yield {**event_data, 'calendar': 'theaterAmsterdam'}


def getEventList():
    url='https://www.theatermascini.nl/'
    events = makeSoup(url).select('.itemscontainer a.itembox')
    return events

def bot():
    from concurrent.futures import ThreadPoolExecutor
    with ThreadPoolExecutor() as executor:
        return (
            gig
            for gigs in executor.map(lambda event: list(getData(event)), getEventList())
            for gig in gigs
        )