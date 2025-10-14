from src.tools.scraper_tools import myStrptime
from src.tools.scraper_tools import makeSoup, makeSeleniumSoup, futureDate
import datetime
import re

# CALENDARS = ['theaterAmsterdam', 'classicalAmsterdam']

def formatDate(dateString):
    vandaag = datetime.date.today()
    morgen = vandaag + datetime.timedelta(days=1)
    dateString = dateString.replace('.','') + " 2024"
    dateString = dateString.replace('Vandaag', vandaag.strftime('%A %d %b'))
    dateString = dateString.replace('Morgen', morgen.strftime('%A %d %b'))

    dateFormat = '%A %d %b om %H:%M %Y'
    date_time = myStrptime(dateString, dateFormat)
    date = futureDate(date_time.date())
    return date.strftime('%Y-%m-%d'), date_time.strftime('%H:%M')

def formatVenue(venue_address):
    venue, address = venue_address.rsplit(', ', 1)
    if address not in ['Haarlem', 'Amsterdam', 'Amstelveen', 'Weesp']:
        raise Exception('unknown locatation: ' + address)
    return venue, address

def formatPrice(pricetag):
    if not pricetag:
        return ""
    pricetag = pricetag.text
    if 'Tickets zijn gratis met de We Are Public-pas' in pricetag:
        return 'free*'
    wap_price = re.search(r'We Are Public-prijs: €\d+(,\d\d)?', pricetag)
    if wap_price:
        print(wap_price[0])
        return wap_price[0].split()[-1].replace(',','.') + "*"
    regulier = re.search(r'Reguliere prijs: €\d+(,\d\d)?', pricetag)
    if regulier:
        print(regulier[0])
        return regulier[0].split()[-1].replace(',','.')
    return ""


def getData(event):
    site = 'https://www.wearepublic.nl' + event.get('href')
    subsoup = makeSoup(site)
    date_time = event.select_one('.event-date').text
    if 'tot' in date_time:
        return
    date, time = formatDate(date_time)
    venue, address = formatVenue(event.select_one('span.event-venue').text.strip())
    try:
        description = subsoup.select_one('main.template__main').text.lower()
    except:
        print('sjldfkjslkdfjldskjflksdjflksjdflkjdslfkj')
        description = makeSeleniumSoup(site, 1).select_one('main.template__main').text.lower()
    if 'jazz' in description:
        return {
            'date': date,
            'time': time,
            'title': event.select_one('h3.event-meta__title').text.strip(),
            'venue': venue,
            'price': formatPrice(subsoup.select_one('.hero__description > p')),
            'site': site,
            'address': address
        }

def getEventList():
    url = 'https://www.wearepublic.nl/alles?region=28'
    load_more = 4 * ["document.getElementsByClassName('event-grid__load-more')[0].click()"]
    events = makeSeleniumSoup(url, 1 , load_more).select('a.event-card')
    if len(events) < 50:
        raise Exception('Fewer events than expected!!!')
    return events[:70]

def bot():
    return map(getData, getEventList())
    # return (gig for event in getEventList() for gig in getData(event))
