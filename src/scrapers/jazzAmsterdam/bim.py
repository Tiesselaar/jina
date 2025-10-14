from src.tools.scraper_tools import makeSoup, myStrptime
import html

def formatDateTime(dateString):
    dateFormat = '%A %d %B %Y %H:%M'
    date = myStrptime(dateString, dateFormat)
    return date.strftime('%Y-%m-%d'), date.strftime('%H:%M')

def formatPrice(price, title):
    if price:
        return "€" + price.replace(',00', '')
    if "Tuesday Jam" in title:
        return "gratis"
    return ""

def getData(event):
    date, time = formatDateTime(event.select_one('start_date_time').text)
    title = html.unescape(event.select_one('title').text)
    eventData = {
        'date': date,
        'time': time,
        'title': title,
        'venue': "Bimhuis",
        'price': formatPrice(event.select_one('price').text, title),
        'site': event.select_one('program_url').text,
        'address': "Piet Heinkade 3, 1019 BR Amsterdam"
    }
    return eventData

def getEventList():
    venue_name = 'bim'
    url = 'https://www.bimhuis.nl/feed/'
    events = makeSoup(url,'xml').select('program_item')
    return events

def bot():
    return map(getData, getEventList())