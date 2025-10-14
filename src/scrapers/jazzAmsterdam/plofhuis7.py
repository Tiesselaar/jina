from src.tools.scraper_tools import myStrptime, makeSoup
import re


def formatDateTime(dateString):
    dateString = dateString.split('-')[0].strip().replace(';',':').replace('.',':')
    if dateString == "":
        return "", ""
    dateFormat = '%d %B %Y: %H:%M uur'
    date = myStrptime(dateString, dateFormat)
    return date.strftime('%Y-%m-%d'), date.strftime('%H:%M')

def formatPrice(eventText):
    price = re.search(r'€ ?\d+([.,](-|\d+))?', eventText)[0]
    price = price.replace('.',',').replace(',00','').replace(',-','').replace(' ','')
    return price

def getData(event):
    if 'jazz' in event.text.lower():
        date, time = formatDateTime(event.select_one('header p').text)
        if date:
            return {
                'date': date,
                'time': time,
                'title': event.select_one('header h3').text,
                'venue': "Plofhuis7 (Weesp)",
                'price': formatPrice(event.text),
                'site': "https://www.uiteraarduitermeer.nl/programma",
                'address': "Uitermeer 3, 1381 HP Weesp"
            }

def getEventList():
    # venue_name for the output file, url for request
    venue_name = 'plofhuis7'
    url = 'https://www.uiteraarduitermeer.nl/programma'
    events = makeSoup(url).select('section.box.special')
    return events

def bot():
    return map(getData, getEventList())



