from src.tools.scraper_tools import myStrptime, futureDate, makeSoup

CALENDARS = ['theaterAmsterdam', 'jazzAmsterdam']

def formatDate(date):
    date += " 2024"
    dateFormat = '%a %d %b %Y'
    myDate = futureDate(myStrptime(date, dateFormat).date())
    return myDate.strftime('%Y-%m-%d')

def formatPrice(price_rows):
    if not price_rows:
        return ""
    price = {
        row.select('td')[0].text.strip(): row.select('td')[-1].text.strip()
        for row in price_rows
    }['normaal']
    return "".join(price.split()).replace(',','.').replace('.00','')

def formatTitle(title, subtitle):
    if subtitle:
        return title + " - " + subtitle
    return title

def getData(event):
    event_data = {
        'date': formatDate(event.select_one('.datetime .date .start').text.strip()),
        'time': event.select_one('.datetime .time .start').text.replace(' uur', '').replace("Vanaf", "").strip().replace('.',':'),
        'title': formatTitle(event.select_one('h3.title').text.strip(),event.select_one('div.subtitle').text.strip()),
        'venue': "De Kleine Komedie",
        'price': formatPrice(event.select('tr')),
        'site': "https://www.dekleinekomedie.nl" + event.select_one('.descMetaContainer a.desc').get('href'),
        'address': "Amstel 56-58, 1017AC Amsterdam"
    }
    if "jazz" in event.text.lower():
        yield {**event_data, 'calendar': 'jazzAmsterdam'}
    yield {**event_data, 'calendar': 'theaterAmsterdam'}

def getEventList():
    url = 'https://www.dekleinekomedie.nl/agenda?max=36&list_type=events&page='
    return (event for page in range(1,6) for event in makeSoup(url + str(page)).select('ul.listItems li.eventCard'))

def bot():
    return (gig for event in getEventList() for gig in getData(event))