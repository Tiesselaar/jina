from src.tools.scraper_tools import myStrptime, makeSoup, futureDate
import re

def parse_date_string(date_string):
    date_list = date_string.split()
    if len(date_list) == 4:
        date_list.insert(1, date_list[-1])
    return " ".join(date_list[:2]), " ".join(date_list[-2:])

def format_date(date_string):
    date_string = parse_date_string(date_string)[0] + " 2020"
    dateFormat = '%d %B %Y'
    date = futureDate(myStrptime(date_string, dateFormat).date(), 30)
    return date.strftime('%Y-%m-%d')

def formatPrice(eventDescription):
    price = re.search(r'(EUR|€) ?\d+(,\d\d)?', eventDescription)
    if not price:
        return ""
    return price[0].replace(' ','').replace('EUR','€')

def getData(event):
    return {
        'date': format_date(event.select_one('.mec-event-month').text),
        'time': event.select_one('.mec-start-time').text,
        'title': event.select_one('.mec-toggle-title').text.strip(),
        'venue': "Kompaszaal",
        'price': formatPrice(event.select_one('.mec-event-content').text),
        'site': 'https://www.kompaszaal.nl/agenda/',
        'address': "KNSM-Laan 311, 1019 LE Amsterdam"
    }

def getEventList():
    venue_name = 'kompaszaal'
    url = 'https://www.kompaszaal.nl/agenda/'
    events = makeSoup(url).select('.mec-toggle-item')
    return events

def bot():
    return map(getData, getEventList())


