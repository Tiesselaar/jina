from src.tools.scraper_tools import myStrptime, makeSoup, futureDate

CALENDARS = ['theaterAmsterdam', 'jazzAmsterdam']

def formatDate(dateString):
    dateString += " 2024"
    dateFormat = '%a %d %b %Y'
    date = myStrptime(dateString, dateFormat).date()
    date = futureDate(date)
    return date.strftime('%Y-%m-%d')

def formatTitle(title, subtitle):
    if subtitle:
        return " - ".join([title,subtitle])
    return title

def formatPrice(price):
    if price:
        price = price.text
    else:
        return ""
    return ''.join(price.split()).replace(',00','')

def getData(event):
    event_data = {
        'date': formatDate(event.select_one('.dateTimeContainer > .dateTimeInner > .datetime > .date > .start').text.strip()),
        'time': event.select_one('.dateTimeContainer > .dateTimeInner > .datetime > .time > .start').text.strip(),
        'title': formatTitle(
            event.select_one('.descMetaContainer > a.desc .title').text,
            event.select_one('.descMetaContainer > a.desc .subtitle').text
        ),
        'venue': 'Theater de Omval',
        'price': formatPrice(event.select_one('.descMetaContainer .meta .price > button')),
        'site': 'https://www.theaterdeomval.nl' + event.select_one('.descMetaContainer > a.desc').get('href'),
        'address': 'Ouddiemerlaan 104, 1111 HL Diemen'
    }
    yield {**event_data, 'calendar': 'theaterAmsterdam'}
    if 'jazz' in event.text.lower():
        yield {**event_data, 'calendar': 'jazzAmsterdam'}

def getEventList():
    css_selector = '.container > .listWrapper > ul.listItems > li > .listItemWrapper > .inner'
    url = 'https://www.theaterdeomval.nl/voorstellingen?list_type=events&max=100&page='
    events = sum((makeSoup(url + str(page)).select(css_selector) for page in range(1,5)), [])
    return events

def bot():
    return (gig for event in getEventList() for gig in getData(event))
