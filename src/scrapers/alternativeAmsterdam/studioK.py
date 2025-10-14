from src.tools.scraper_tools import myStrptime
from src.tools.scraper_tools import makeSoup, futureDate

# CALENDARS = ['theaterAmsterdam', 'classicalAmsterdam']

def formatDate(dateString):
    dateString += " 2024"
    dateFormat = '%d %B %Y'
    date = myStrptime(dateString, dateFormat).date()
    date = futureDate(date, 30)
    return date.strftime('%Y-%m-%d')

def formatPrice(price):
    price = price.text if price else ""
    if "gratis" in price.lower():
        return "free"
    price = price.replace(' ','')
    return price

def getData(event):
    details = {
        row.select_one('td > strong').text: row.select('td')[1]
        for row in event.select('.row-details .txt > table tr')
    }
    return {
        'date': formatDate(details["Datum:"].text),
        'time': details["Tijd:"].text.split("-")[0].strip(),
        'title': event.select_one('.title h2').text,
        'venue': "Studio/K",
        'price': formatPrice(details.get("Prijs:")),
        'site': event.select_one('a.moretag').get('href'),
        'address': "Timorplein 62, 1094 CC Amsterdam, Nederland"
    }

def getEventList():
    url = 'https://studio-k.nu/events/'
    events = makeSoup(url).select('.events-lijst ul li')
    return events

def bot():
    return map(getData, getEventList())
    # return (gig for event in getEventList() for gig in getData(event))
