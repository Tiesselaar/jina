from src.tools.scraper_tools import myStrptime
from src.tools.scraper_tools import makeSoup, futureDate

# CALENDARS = ['theaterAmsterdam', 'classicalAmsterdam']

def formatDate(dateString):
    dateString += " 2024"
    dateFormat = '%a %d %b %Y'
    date = myStrptime(dateString, dateFormat).date()
    date = futureDate(date)
    return date.strftime('%Y-%m-%d')

def formatPrice(info_lines):
    for li in info_lines:
        if li.contents and li.contents[0].text == "Regulier:":
            return li.contents[1].strip().replace(" ","")
    return ""

def getData(event):
    site = "https://ccamstel.nl" + event.select_one('a[href^="/programma"]').get('href')
    price = formatPrice(makeSoup(site).select('ul.info-list li'))
    dates = event.select('.dates-block > div.row > div')
    for date in dates:
        yield {
            'date': formatDate(date.select_one('ul').contents[0].strip()),
            'time': date.select_one('ul span').text,
            'title': event.select_one('h2.performace-title').text + " - " + event.select_one('h2.performace-title + p.light').text,
            'venue': "CC-Amstel",
            'price': price,
            'site': site,
            'address': "Cullinanplein 1, 1074 JN Amsterdam",
        }

def getEventList():
    url = 'https://ccamstel.nl/programma/'
    events = makeSoup(url).select('#overzicht .items-holder .item')
    return events

def bot():
    return (gig for event in getEventList() for gig in getData(event))
