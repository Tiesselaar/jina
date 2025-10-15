from src.tools.scraper_tools import myStrptime, makeSoup
import re

CALENDARS = ['jazzAmsterdam', 'classicalAmsterdam', 'booksAmsterdam']

def formatDateTime(dateString):
    dateString = dateString.split('-')[0].strip().replace(';',':').replace('.',':')
    if dateString == "":
        return "", ""
    dateFormat = '%d %B %Y %H:%M uur'
    date = myStrptime(dateString, dateFormat)
    return date.strftime('%Y-%m-%d'), date.strftime('%H:%M')

def formatPrice(eventText):
    price = re.search(r'€ ?\d+([.,](-|\d+))?', eventText)
    if price:
        price = price[0]
    else:
        return ""
    price = price.replace('.',',').replace(',00','').replace(',-','').replace(' ','')
    return price

def getData(event):
    date, time = formatDateTime(event.select_one('header p').text)
    if not date:
        print(event.select_one('header h3').text)
        return
    
    event_data = {
        'date': date,
        'time': time,
        'title': event.select_one('header h3').text.strip(),
        'venue': "Plofhuis7 (Weesp)",
        'price': formatPrice(event.text),
        'site': "https://www.uiteraarduitermeer.nl/programma",
        'address': "Uitermeer 3, 1381 HP Weesp"
    }
    if 'jazz' in event.text.lower() or "Joris Teepe" in event.text:
        yield {**event_data, "calendar": "jazzAmsterdam"}
    elif 'muziek' in event.text.lower() or 'concert' in event.text.lower():
        yield {**event_data, "calendar": "classicalAmsterdam"}
    else:
        yield {**event_data, "calendar": "booksAmsterdam"}


def getEventList():
    # venue_name for the output file, url for request
    venue_name = 'plofhuis7'
    url = 'https://www.uiteraarduitermeer.nl/programma'
    events = makeSoup(url).select('section.box.special')
    return events

def bot():
    return (gig for event in getEventList() for gig in getData(event))

