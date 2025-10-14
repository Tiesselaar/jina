from src.tools.scraper_tools import myStrptime
from src.tools.scraper_tools import makeSoup, makeSeleniumSoup, futureDate

CALENDARS = ['popAmsterdam', 'jazzAmsterdam']

def formatDate(dateString):
    dateString += " 2024"
    dateFormat = '%a. %d %b %Y'
    date = myStrptime(dateString, dateFormat).date()
    date = futureDate(date)
    return date.strftime('%Y-%m-%d')

def getData(event):
    title = event.select_one('.titel2 > .wp_theatre_event_title > a').text
    if "Club Dauphine Is Gesloten" in title:
        return None
    shop = event.select_one('.tickets a.wp_theatre_event_tickets_url').get('href')
    subsoup = makeSeleniumSoup(shop, waitFor='.ticket-text.item-price__test')
    eventData = {
        'date': formatDate(event.select_one('.datum2 > .wp_theatre_event_date.wp_theatre_event_startdate').text),
        'time': event.select_one('.datum2 > .wp_theatre_event_time.wp_theatre_event_starttime').text,
        'title': title.replace("Club Dauphine - ", "").split(' - ')[0],
        'venue': "Club Dauphine",
        'price': subsoup.select_one('.ticket-text.item-price__test > span').text.replace(" ", ""),
        'site': event.select_one('.titel2 > .wp_theatre_event_title > a').get('href'),
        'address': "Prins Bernhardplein 175, 1097 BL Amsterdam"
    }
    yield {**eventData, 'calendar': 'popAmsterdam'}
    yield {**eventData, 'calendar': 'jazzAmsterdam'}

def getEventList():
    url = 'https://clubdauphine.nl/agenda/'
    events = makeSoup(url).select('.wp_theatre_event')
    return events

def bot():
    return (gig for event in getEventList() for gig in getData(event))
