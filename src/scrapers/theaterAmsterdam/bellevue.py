from src.tools.scraper_tools import myStrptime, futureDate
from src.tools.scraper_tools import makeSoup

def formatDate(dateString):
    dateString += " 2024"
    dateFormat = '%a %d %b %Y'
    date = myStrptime(dateString, dateFormat).date()
    date = futureDate(date,30)
    return date.strftime('%Y-%m-%d')

def formatPrice(price):
    if price:
        return "".join(price.text.split()).replace(',00','')
    return ""

def formatTitle(title, subtitle):
    if subtitle:
        return title + " - " + subtitle
    return title

def getData(event):
    site = "https://www.theaterbellevue.nl" + event.select_one('.descMetaContainer > a.desc').get('href')
    try:
        if "Expositie" in event.select_one('.supertitle').text:
            print('lskfdjslkdfjslkdfjsldkj')
            return
    except:
        pass
    return {
        'date': formatDate(event.select_one('.top-date > span.start').text.strip()),
        'time': event.select_one('.top-date > span.time').text.split()[0],
        'title': formatTitle(event.select_one('h2.title').text.strip(),event.select_one('div.subtitle').text.strip()),
        'venue': "Theater Bellevue",
        'price': formatPrice(event.select_one('.price > button.pricePopoverBtn')),
        'site': site,
        'address': "Leidsekade 90, 1017 PN Amsterdam"
    }

def getEventList():
    url = 'https://www.theaterbellevue.nl/agenda?list_type=events&max=36&page='
    return (event for page in range(1,3) for event in makeSoup(url + str(page)).select('ul.listItems li.eventCard'))

def bot():
    return map(getData, getEventList())