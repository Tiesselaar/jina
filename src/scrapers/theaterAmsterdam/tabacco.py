from src.tools.scraper_tools import myStrptime
from src.tools.scraper_tools import makeSeleniumSoup
from datetime import timedelta

CALENDARS = ['theaterAmsterdam', 'jazzAmsterdam']

def format_one_date(dateString):
    dateFormat = '%d/%m/%Y'
    return myStrptime(dateString, dateFormat).date()

def format_date(date_string):
    if "-" in date_string:
        from_date, until_date = [format_one_date(date_part) for date_part in date_string.split(" - ")]
        time_delta = until_date - from_date
        return [(from_date + timedelta(day)).strftime('%Y-%m-%d') for day in range(time_delta.days + 1)]
    else:
        return([format_one_date(date_string).strftime('%Y-%m-%d')])

def format_time(lines):
    try:
        return lines['Start show']
    except:
        return lines['Deuren open']

def getData(event):
    site = event.get('href')
    print(site)
    subsoup = makeSeleniumSoup(site)
    lines = dict([[cell.text for cell in line.select('div')] for line in subsoup.select('aside > div > div')])
    
    event_data =  {
        'time': format_time(lines),
        'title': subsoup.select_one('h1').text.strip(),
        'venue': 'TOBACCO Theater',
        'price': "",
        'site': site,
        'address': "Nes 75-87, 1012 KD Amsterdam"
    }
    for date in format_date(lines['Datum']):
        yield {'date': date, **event_data, 'calendar': 'theaterAmsterdam'}
        if 'jazz' in subsoup.select_one('section.ll-section--event_introduction').text.lower():
            yield {'date': date, **event_data, 'calendar': 'jazzAmsterdam'}
    

def getEventList():
    url = 'https://tobacco.nl/programma/'
    events = makeSeleniumSoup(url).select('a[title^="Link to event"]')
    return events

def bot():
    return (gig for event in getEventList() for gig in getData(event))
