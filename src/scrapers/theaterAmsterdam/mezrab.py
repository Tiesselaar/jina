from src.tools.scraper_tools import myStrptime
from src.tools.scraper_tools import makeSoup, futureDate

# CALENDARS = ['theaterAmsterdam', 'classicalAmsterdam']

def formatDate(dateString):
    dateString += " 2024"
    dateFormat = '%a %d.%m %Y'
    date = myStrptime(dateString, dateFormat).date()
    date = futureDate(date)
    return date.strftime('%Y-%m-%d')

def getLocation(event):
    location = event.select_one('.locationhomepage')
    if location:
        if "The Other Mezrab" in location.text:
            return "The Other Mezrab", "De Wittenstraat 27, 1054AK Amsterdam"
        else:
            raise Exception("Unknown location: " + location.text)
    else:
        return "Mezrab", "Veemkade 576, 1019 BL Amsterdam"

def getData(event):
    venue, address = getLocation(event)
    return {
        'date': formatDate(event.select_one('td.eventtd24').text.split("|")[0].strip()),
        'time': event.select_one('td.eventtd24').text.split("|")[1].strip(),
        'title': event.select_one('a').text,
        'venue': venue,
        'price': "",
        'site': event.select_one('a').get('href'),
        'address': address,
    }

def getEventList():
    url = 'https://mezrab.nl/full-program/'
    events = makeSoup(url).select('.elementor-widget-container .em-events-widget table.tableeventd')
    return events

def bot():
    return map(getData, getEventList())
    # return (gig for event in getEventList() for gig in getData(event))
