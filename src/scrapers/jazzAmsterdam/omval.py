from src.tools.scraper_tools import myStrptime, makeSoup, futureDate

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
    return ''.join(price.split()).replace(',00','')

def getData(event):
    if 'jazz' in event.text.lower():
        return {
            'date': formatDate(event.select_one('.dateTimeContainer > .dateTimeInner > .datetime > .date > .start').text.strip()),
            'time': event.select_one('.dateTimeContainer > .dateTimeInner > .datetime > .time > .start').text.strip(),
            'title': formatTitle(
                event.select_one('.descMetaContainer > a.desc .title').text,
                event.select_one('.descMetaContainer > a.desc .subtitle').text
            ),
            'venue': 'Theater de Omval',
            'price': formatPrice(event.select_one('.descMetaContainer .meta .price > button').text),
            'site': 'https://www.theaterdeomval.nl' + event.select_one('.descMetaContainer > a.desc').get('href'),
            'address': 'Ouddiemerlaan 104, 1111 HL Diemen'
        }

def getEventList():
    css_selector = '.container > .listWrapper > ul.listItems > li > .listItemWrapper > .inner'
    url = 'https://www.theaterdeomval.nl/voorstellingen/muziek?page='
    events = sum((makeSoup(url + str(page)).select(css_selector) for page in range(1,5)), [])
    return events

def bot():
    return map(getData, getEventList())