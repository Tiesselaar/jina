from src.tools.scraper_tools import myStrptime
from src.tools.scraper_tools import makeSeleniumSoup, futureDate

CALENDARS = ['theaterAmsterdam', 'classicalAmsterdam']

def formatDate(dateString):
    dateString += " 2024"
    dateFormat = '%A %d %B %Y'
    date = myStrptime(dateString, dateFormat).date()
    date = futureDate(date)
    return date.strftime('%Y-%m-%d')

def formatVenue(event):
    if "in het Orgelpark" in event.text:
        return "Orgelpark", "Gerard Brandtstraat 26, 1054 JK Amsterdam"
    if "in de OBA Oosterdok" in event.text:
        return "OBA Oosterdok", "Oosterdokskade 143, 1011 DL Amsterdam"
    allowed_text = event.text
    allowed_text = allowed_text.replace("in collaboration","")
    allowed_text = allowed_text.replace("in de overgang","")
    allowed_text = allowed_text.replace("Amsterdammers in Oost","")
    allowed_text = allowed_text.replace("Queer in Oost","")
    allowed_text = allowed_text.replace("To believe in MagicRosa","")
    allowed_text = allowed_text.replace("Transformation in Motion","")

    if " in " in allowed_text:
        raise Exception("unkown location?: " + event.text)
    return "Pleintheater", "Sajetplein 39, 1091DB Amsterdam"


def getData(date_event):
    date, event = date_event
    venue, address = formatVenue(event)
    event_data = {
        'date': formatDate(date.text.strip()),
        'time': event.select_one('.meta').text.split('//')[1].strip().rjust(5,'0'),
        'title': event.select_one('.title').text.strip(),
        'venue': venue,
        'price': "".join(event.select_one('.meta').text.split('//')[2].split()[:2]),
        'site': 'https://www.plein-theater.nl' + event.get('href'),
        'address': address
    }
    if "concert" in event.select_one('.meta').text.split('//')[0].strip().lower():
        yield {**event_data, 'calendar': 'classicalAmsterdam'}
    yield {**event_data, 'calendar': 'theaterAmsterdam'}

def getEventList():
    url = 'https://www.plein-theater.nl/agenda'
    headers_events = makeSeleniumSoup(url, 2).select('#agenda :is(.header, a.event)')
    if len(headers_events) == 0:
        raise Exception("Fewer gigs than expected...")
    events = []
    for h_event in headers_events:
        if 'header' in h_event.get('class'):
            date = h_event
        else:
            events.append([date, h_event])
    return events

def bot():
    return (gig for event in getEventList() for gig in getData(event))


