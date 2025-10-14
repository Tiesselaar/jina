from src.tools.scraper_tools import myStrptime
from src.tools.scraper_tools import makeSoup, futureDate

CALENDARS = ['theaterAmsterdam', 'jazzAmsterdam']

def formatDate(date_string):
    date_string = date_string.strip()
    dateFormats = [
        '%d / %m / %Y - %H:%M',
        '%d / %m / %Y - %I%p',
        '%d / %m / %Y - %I %p',
        '%d / %m / %Y - %I.%M%p',
        '%d / %m / %Y - %I.%M %p',
        '%d / %m / %Y - %I.%M',
    ]
    for dateFormat in dateFormats:
        try:
            date = myStrptime(date_string, dateFormat)
            break
        except:
            continue
    try:
        date
    except:
        try: 
            date = myStrptime(date_string, '%d / %m / %Y')
            return "", ""
        except:
            raise Exception("Unhandled date format: " + date_string)
    return date.strftime('%Y-%m-%d'), date.strftime('%H:%M')

def getData(event):
    date_strings = map(lambda tag: tag.text, event.select('.title .date'))
    for date, time in (formatDate(date_string) for date_string in date_strings if date_string):
        if date == "":
            print("No time in date string")
            continue
        event_data = {
            'date': date,
            'time': time,
            'title': event.select_one('.title > h3').text,
            'venue': "Het Badhuistheater",
            'price': "",
            'site': event.get('href'),
            'address': "Boerhaaveplein 28, 1091 AT Amsterdam",
        }
        yield {**event_data, 'calendar': "theaterAmsterdam"}
        if "jazz" in event.text.lower():
            yield {**event_data, 'calendar': "jazzAmsterdam"}



def getEventList():
    url = 'https://www.badhuistheater.nl/agenda/'
    events = makeSoup(url).select('section.events a.event-thumb')
    return events

def bot():
    return (gig for event in getEventList() for gig in getData(event))
