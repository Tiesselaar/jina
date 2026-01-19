from src.tools.scraper_tools import myStrptime
from src.tools.scraper_tools import makeSoup

def formatDate(dateString):
    if "-" in dateString:
        dateString = dateString.split()
        if len(dateString) != 6:
            raise Exception('Unknown date format: ' + " ".join(dateString))
        dateString = " ".join(dateString[:2]) + " " + dateString[-1]
    dateFormat = '%d %B %Y'
    date = myStrptime(dateString, dateFormat).date()
    return date.strftime('%Y-%m-%d')

def formatTime(time):
    if time:
        time = time.contents[0]
    else:
        return "09:00", " - incorrect starting time. Check website!"
    if time == "All Day":
        return "09:00", " - all day event. Check times on the website!"
    return time.split("-")[0].strip(), ""

def formatLocation(location):
    if location == "Café de Druif":
        return "Café de Druif", "Rapenburgerplein 83, 1011 VJ Amsterdam, Nederland"
    if "No Limit’s Art Castle!" in location:
        return "No Limits! Art Castle", "Sint Annendwarsstraat 9 C, 1012 HC Amsterdam, Nederland"
    if location == "The Fat Mermaid":
        return "The Fat Mermaid", "Strand Noord 19, 2586 ZZ Den Haag, Nederland"
    if "Oedipus Craft Space" in location:
        return "Oedipus Craft Space", "Schaafstraat 21, 1021 KD Amsterdam"
    if location == "Bordello Aperitivo":
        return "Bordello Aperitivo", "Zeedijk 41, 1012 AR Amsterdam, Nederland"
    if location == "Pip Den Haag":
        return "Pip", "Binckhorstlaan 36, 2516 BE Den Haag, Nederland"
    if location == "Marineterrein Amsterdam":
        return "Marineterrein", "Kattenburgerstraat 5, 1018 JA Amsterdam, Nederland"
    if location == "Homomonument":
        return "Homomonument", "Westermarkt, 1016 DW Amsterdam, Nederland"
    if location == "NACHBAR":
        return "nachbar", "Nieuwezijds Voorburgwal 169, 1012 RK Amsterdam, Nederland"
    if location == "Proeflokaal ‘t Nieuwe Diep":
        return "Proeflokaal 't Nieuwe Diep", "Flevopark 13a, 1095 KE Amsterdam, Nederland"
    if location == "Paleis van de Weemoed":
        return "Paleis van de Weemoed", "Oudezijds Voorburgwal 15, 1012 EH Amsterdam"
    if location == "Café Schiller":
        return "Café Schiller", "Rembrandtplein 24-A, 1017 CV Amsterdam"
    if location == "PARADISO":
        return "Paradiso", "Weteringschans 6-8, 1017 SG Amsterdam"
    if location in ["SEXYLAND SHOP", "LET’S GO", "TBA"]:
        return None, None

    raise Exception('Unkown location: "{}"'.format(location))

def getData(event):
    title = event.select_one('.information .title').contents[0]
    if title == "SEXYLAND TRAM":
        return
    if title.lower() == "past events":
        return
    venue, address = formatLocation(event.select_one('.information .location').contents[0])
    if not venue:
        return
    if "Den Haag" in address:
        return
    time, all_day = formatTime(event.select_one('.information .time'))
    return {
        'date': formatDate(event.select_one('.information .date').contents[0]),
        'time': time,
        'title': title + all_day,
        'venue': venue,
        'price': "",
        'site': "https://sexyland.world/projects/events/",
        'address': address
    }

def getEventList():
    url = 'https://sexyland.world/projects/events/'
    events = makeSoup(url).select('.container-events .matrix-event')
    return events

def bot():
    return map(getData, getEventList())
    # return (gig for event in getEventList() for gig in getData(event))
