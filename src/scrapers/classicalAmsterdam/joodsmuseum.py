from src.tools.scraper_tools import myStrptime
from src.tools.scraper_tools import makeSoup, futureDate
import re

CALENDARS = ['classicalAmsterdam']

def formatDate(dateString):
    dateString += " 2024"
    dateFormat = '%d %B %Y'
    date = myStrptime(dateString, dateFormat).date()
    date = futureDate(date, failOnFarFuture=False)
    return date.strftime('%Y-%m-%d')

def get_location(info, more_info):
    if "Locatie: Portugese Synagoge" in info:
        return "Portugese Synagoge", "Mr. Visserplein 3, 1011 RD Amsterdam"
    elif "Locatie: Joods Museum" in info:
        return "Joods Museum", "Nieuwe Amstelstraat 1, 1011 PL Amsterdam"
    elif "Locatie: Hollandsche Schouwburg" in info:
        return "Hollandsche Schouwburg", "Plantage Middenlaan 24, 1018 DE Amsterdam"
    elif "Locatie: de Uilenburgersjoel" in info:
        return "Uilenburgersjoel", "Nieuwe Uilenburgerstraat 91, 1011 LM Amsterdam"
    elif "Locatie: Rode Hoed" in info:
        return "Rode Hoed", "Keizersgracht 102, 1015 CV Amsterdam"
    elif "in het Joods Museum" in more_info:
        return "Joods Museum", "Nieuwe Amstelstraat 1, 1011 PL Amsterdam"
    else:
        raise Exception('Unknown location')

def format_price(more_info):
    try:
        return '€' + re.search(r"Toegang: € \d+[\.,]\d+", more_info)[0].split()[-1].replace(',','.').replace('.00','')
    except:
        return ""

def getData(event):
    site = "https://jck.nl" + event.select_one('a.agenda-item').get('href')
    print(site)
    subsoup = makeSoup(site)
    info = subsoup.select_one('.section--info-list').text
    more_info = "\n\n".join(section.text for section in subsoup.select(':is(.section--rich-text, .rich-text)'))
    venue, address = get_location(info, more_info)
    return {
        'date': formatDate(event.select_one('.base-card__meta .meta-line__after').text),
        'time': re.search(r'Tijd:( aanvang)? (\d\d.\d\d)', info).group(2).replace('.',':'),
        'title': event.select_one('h4.base-card__title').text,
        'venue': venue,
        'price': format_price(subsoup.text),
        'site': site,
        'address': address
    }

def getEventList():
    urls = {
        'classicalAmsterdam': 'https://jck.nl/agenda?type-event=concert',
        # 'theaterAmsterdam': 'https://jck.nl/agenda?type-event=programma'
    }
    return {
        calendar: makeSoup(urls[calendar]).select('li.agenda-overview__list__item')
        for calendar in CALENDARS
    }

def bot():
    return (
        {**getData(event), 'calendar': calendar}
        for calendar in CALENDARS
        for event in getEventList()[calendar]
    )
