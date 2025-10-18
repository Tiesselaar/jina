from src.tools.scraper_tools import myStrptime
from src.tools.scraper_tools import makeSoup, futureDate

def formatPrice(ticket_box):
    if "Geen kaarten (meer) beschikbaar" in ticket_box.text:
        return "s.o."
    try:
        price = ticket_box.select_one('strong.js-price-display').text
        price = price.replace(' ','').replace(',','.')
        return price
    except:
        return ""


def getData(event):
    site = 'https://krakeling.nl' + event.select_one('a').get('href')
    venue = None
    address = None
    if event.select_one('.event-card__is-at-external-location-label'):
        if "-krakeling-rietwijker" in site:
            venue = "De Rietwijker"
            address = "Parlevinker 9, 1034 PX Amsterdam"
        elif "-munganga-krakeling" in site:
            venue = "Teatro Munganga"
            address = "Schinkelhavenstraat 27-HS, 1075 VP Amsterdam"
        elif "-meervaart" in site:
            venue = "Theater de Meervaart"
            address = "Meer en Vaart 300, 1068 LE Amsterdam, Nederland"
        elif "-bijlmer-parktheater" in site:
            venue = "Bijlmer Parktheater"
            address = "Anton de Komplein 240, 1102 DR Amsterdam"
        elif "-podium-mozaiek" in site:
            venue = "Podium Mozaïek"
            address = "Bos en Lommerweg 191, 1055 DT Amsterdam"
        elif "munganga-" in site:
            venue = "Munganga Theater"
            address = "Schinkelhavenstraat 27-HS, 1075 VP Amsterdam, Nederland"
        elif "rietwijker-" in site:
            venue = "De Rietwijker"
            address = "Parlevinker 9, 1034 PX Amsterdam, Nederland"
        # elif "hassan-en-moos" in site:
        #     venue = "ROC Amsterdam - MBO College Centrum"
        #     address = "Elandsstraat 175, 1016 SB Amsterdam"
        else:
            raise Exception('unknown location: ' + site)
        
    return {
        'date': event.select_one('time').get('datetime')[:10],
        'time': event.select_one('time').get('datetime')[11:16],
        'title': event.select_one('.event-card__title').text,
        'venue': venue or "Theater De Krakeling",
        # the following line makes it very slow:
        'price': formatPrice(makeSoup(site).select_one('aside.ticket-box')),
        'site': site,
        'address': address or "Pazzanistraat 15, 1014 DB Amsterdam"
    }

def getEventList():
    url = 'https://krakeling.nl/programma'
    return makeSoup(url).select('section.event-list ul.event-list__content li.event-list__item')[:50]

def bot():
    return map(getData, getEventList())
