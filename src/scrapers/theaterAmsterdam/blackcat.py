from src.tools.scraper_tools import myStrptime
from src.tools.scraper_tools import makeSoup, makeSeleniumSoup, futureDate

def formatDate(dateString):
    dateString += " 2024"
    dateFormat = '%a %d %b %Y'
    date = myStrptime(dateString, dateFormat).date()
    date = futureDate(date)
    return date.strftime('%Y-%m-%d')

def getData(site):
    subsoup = makeSoup(site)
    event_data =  {
        'title': subsoup.select_one('h1.page-default-title').text + f" ({subsoup.select_one('.event-tag.leeftijd').text})",
        'venue': 'Black Cat Theater',
        'site': site,
        'address': 'Schakelstraat 2, 1014 AW Amsterdam'
    }
    for ticket in subsoup.select_one('#event-tickets').select('.event-summary'):
        yield {
            **event_data,
            'date': formatDate(ticket.select_one('.date > .info').text),
            'time': ticket.select_one('.time > .info').text,
            'price': ticket.select_one('.price > .info > span').text.replace(' ','')
        }

def getEventList():
    url = 'https://blackcattheatre.nl/agenda-van-kindertheater-black-cat-theatre/'
    soup = makeSeleniumSoup(url, 1)
    calendar = soup.select_one('#event-tickets')
    if calendar:
        events = list(set((link.get('href')) for link in calendar.select('.event-summary a.title')))
    elif "SUMMER BRAKE" in soup.text:
        return []
    else:
        raise ValueError("No events found or the page structure has changed.")
    return events

def bot():
    return (gig for event in getEventList() for gig in getData(event))
