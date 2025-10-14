from src.tools.scraper_tools import myStrptime, makeSoup, makeSeleniumSoup
import re

def formatDate(dateString):
    if re.match(r'Date: \w+ \d\d? & \d\d?, \d\d\d\d', dateString):
        month, day1, day2, year = dateString.replace('Date:', '').replace(',','').replace('&','').split()
        dates_strings = [' '.join([month, day, year]) for day in [day1, day2]]
    elif re.match(r'Date: \w+ \d\d?, \d\d\d\d', dateString):
        dates_strings = [dateString.replace('Date: ', '').replace(',','')]
    date_format = '%B %d %Y'
    dates = [myStrptime(new_date_string, date_format).date() for new_date_string in dates_strings]
    return [date.strftime('%Y-%m-%d') for date in dates]

def formatTime(timeString):
    return timeString[6:11]

def formatPrice(price):
    for i in range(1,10):
        price = price.replace(f',{i}0', f',{i}')
    return price.replace(',00', '').replace(" ", "").lower().replace('.',',')

def getData(event):
    print(event)
    subsoup = makeSoup(event)
    info_lines = [x.text for x in subsoup.select('span.elementor-icon-list-text')]
    dates = formatDate([x for x in info_lines if "Date: " in x][0])
    eventData = {
        'time': formatTime([x for x in info_lines if "Time: " in x][0]),
        'title': subsoup.select_one('h3.elementor-heading-title').text.strip(),
        'venue': "ZOJazz Stage",
        'price': "",
        'site': event,
        'address': "Bijlmerplein 888, 1102 MG Amsterdam"
    }
    try:
        widgetURL = makeSeleniumSoup(event, 1).select_one('div[id^=eventbrite-widget-container] iframe').get('src')
        eventbriteSoup = makeSoup(widgetURL)
        eventData['price'] = formatPrice(eventbriteSoup.select_one('[data-testid="ticket-price__price"]').text)
    except:
        pass
    for date in dates:
        yield {'date': date, **eventData}
    
def getEventList():
    url = 'https://www.zojazzstage.com/events/'
    event_elts = makeSoup(url).select('a.elementor-button[href^="https://www.zojazzstage.com/event"]')
    events = list(set([x.get("href") for x in event_elts]))
    return events

def bot():
    return (gig for event in getEventList() for gig in getData(event))