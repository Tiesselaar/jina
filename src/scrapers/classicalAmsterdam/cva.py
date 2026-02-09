from src.tools.scraper_tools import myStrptime, makeSoup
import re

CALENDARS = ['jazzAmsterdam', 'classicalAmsterdam', 'popAmsterdam']

def formatDate(date_time_string):
    dateFormat = ' %d.%m.%y, %H:%M uur '
    date_time = myStrptime(date_time_string, dateFormat)
    return date_time.strftime('%Y-%m-%d'), date_time.strftime('%H:%M')

def formatPrice(description, venue):
    eventPrice = re.search(r"€ ?\d+(.\d\d\d)*([.,](\d\d?|-))?", description)
    if eventPrice:
        return eventPrice[0].replace(",-","").replace(" ", "").replace('.000','k')
    elif "Blue Stage" in venue:
        return "gratis"
    else:
        return ""

def getData(event_calendar):
    event, calendar = event_calendar
    title = event.select_one('.agenda-list-title').text.strip()
    if title == "Jazz | Jazzfest Amsterdam":
        return
    date, time = formatDate(event.select_one('.agenda-list-date').text)
    venue = event.select_one('.location').text.replace('Conservatorium van Amsterdam', 'CvA')
    site = 'https://www.conservatoriumvanamsterdam.nl' + event.select_one('a').get('href')
    subsoup = makeSoup(site)
    description = subsoup.select_one('#main-content .calendar.event.row .text')
    description = description.text if description else ""
    location = subsoup.select_one('#main-content .calendar.event.row .calendar-event-location')
    tag = {
        "jazzAmsterdam": "Jazz",
        "classicalAmsterdam": "Klassiek",
        "popAmsterdam": "Pop",
    }
    title = title.replace(tag[calendar] + ' | ', '')
    print(title)
    return {
        'date': date,
        'time': time,
        'title': title,
        'venue': venue,
        'price': formatPrice(description, venue),
        'site': site,
        'address': location.select_one('.calendar-event-address').text + ', ' + location.select_one('.calendar-event-city').text,
        'calendar': calendar,
    }

def getEventList():
    url = {
        "jazzAmsterdam": "https://www.conservatoriumvanamsterdam.nl/agenda/jazz",
        "classicalAmsterdam": "https://www.conservatoriumvanamsterdam.nl/agenda/klassiek",
        "popAmsterdam": "https://www.conservatoriumvanamsterdam.nl/agenda/pop",
    }
    return [[event, calendar] for calendar in CALENDARS for event in makeSoup(url[calendar]).select('.agenda-list-event')]

def bot():
    from concurrent.futures import ThreadPoolExecutor
    with ThreadPoolExecutor() as executor:
        results = list(executor.map(getData, getEventList()))
    return results
