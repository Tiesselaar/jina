from src.tools.scraper_tools import myStrptime
from src.tools.scraper_tools import makeSoup, makeSeleniumSoup, futureDate

def formatDate(dateString):
    dateString = " ".join(dateString.split()).replace('.','')
    dateString += " 2024"
    dateFormat = '%a %d %b %Y'
    date = myStrptime(dateString, dateFormat).date()
    date = futureDate(date)
    return date.strftime('%Y-%m-%d')

def get_ticket_price(url):
    if "tickets.debalie.nl" in url:
        ticket_link = url
    else:
        ticket_link = makeSoup(url).select_one('iframe.active-tickets-iframe__iframe').get('src')
    tickets = makeSeleniumSoup(ticket_link).select('li.at-shopping-cart-orderrow')
    tickets = [ticket for ticket in tickets if "Midden" in ticket.text or "Regulier" in ticket.text or "Middle" in ticket.text]
    regulier, = tickets
    return regulier.select_one('.at-shopping-cart-label-inner-name-price').text.replace(',','.').replace(' ','').replace('.00','')
    

def formatPrice(button):
    button_text = button.text.lower().strip()
    if button_text == 'gratis':
        return('free')
    elif button_text == 'besloten':
        return "private"
    elif button_text == 'uitverkocht':
        return "s.o."
    elif button_text == 'tickets':
        return get_ticket_price(button.get('href'))
    else:
        return ""

def get_location(subsoup):
    try:
        location = subsoup.select_one('.banner-bar span.banner-bar__time').text.split('/')[-1].strip()
    except:
        return 'Balie', 'Kleine-Gartmanplantsoen 10, 1017 RR Amsterdam'
    if location in ['Salon', 'Grote Zaal', 'Pleinzaal', 'Filmzaal']:
        return 'Balie', 'Kleine-Gartmanplantsoen 10, 1017 RR Amsterdam'
    elif location in ['Rotterdam', 'Groningen', 'Cultura Ede', 'Paardenkathedraal, Utrecht']:
        return None, None
    else:
        raise Exception('Unknown location, planned but probably to strict error: ' + location)

def getData(event):
    site = event.select_one('.agenda-item__details > .agenda-item__title-wrapper > a').get('href')
    print(site)
    subsoup = makeSoup(site)
    venue, address = get_location(subsoup)
    if not venue or not address:
        return
    price = formatPrice(event.select('.agenda-item__actions a.button')[-1])
    if price == "private":
        return
    return {
        'date': formatDate(event.select_one('.agenda-item__stroke span.date').text.split('/')[0]),
        'time': event.select_one('.agenda-item__stroke span.date').text.split('/')[1].strip(),
        'title': event.select_one('.agenda-item__details > .agenda-item__title-wrapper > h3').text,
        'venue': venue,
        'price': price,
        'site': site,
        'address': address
    }

def getEventList():
    url = 'https://debalie.nl/programma/'
    events = makeSeleniumSoup(url).select('section.agenda article.agenda-item')
    return events

def bot():
    return map(getData, getEventList())