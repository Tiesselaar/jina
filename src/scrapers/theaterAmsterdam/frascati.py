from src.tools.scraper_tools import myStrptime
from src.tools.scraper_tools import makeSoup, futureDate

# CALENDARS = ['theaterAmsterdam', 'classicalAmsterdam']

def formatDate(dateString):
    dateFormat = '%a %d %b ’%y'
    date = myStrptime(dateString, dateFormat).date()
    return date.strftime('%Y-%m-%d')

# def formatTime(time):
#     # format time as '21:00'
#     return time

def formatPrice(price_rows):
    if not price_rows:
        return ""
    price = {
        row.select('td')[0].text.strip(): row.select('td')[-1].text.strip()
        for row in price_rows
    }['Standaard']
    return "".join(price.split()).replace(',','.').replace('.00','')

def formatTitle(title, subtitle):
    if subtitle:
        return title + " - " + subtitle
    return title





def formatLocation(location, venue):
    # These are (rare) exceptions. I'll treat them one-by-one
    if not location:
        if venue.text.strip() == "CC Amstel, Amsterdam":
            return "CC Amstel", "Cullinanplein 1, 1074 JN Amsterdam"
        elif venue.text.strip() == "Theater De Landing, Amstelveen":
            return "Theater De Landing", "Uilenstede 106, 1183 AM Amstelveen"
        elif venue.text.strip() in ["Studio 1", "Studio 2", "Studio 3"]:
            return "Frascati", "Nes 63, 1012 KD Amsterdam"
        elif "Het Spektakeltje" in venue.text:
            return None, None
        elif "Het Nationale Theater" in venue.text:
            return None, None
        elif "IDRA Teatro" in venue.text:
            return None, None
        else:
            raise Exception('Unhandled case of missing location: ' + venue.text.strip())
    location = location.text.strip()
    if 'Amsterdam' not in location:
        if "Amsterdam" in venue.text:
            if "de kleine komedie, amsterdam" in venue.text.lower():
                return "De Kleine Komedie", "Amstel 56-58, 1017 AC  AMSTERDAM"
            if "Dominicuskerk" in venue.text:
                return "Dominicuskerk", "Spuistraat 12, 1012 TS Amsterdam"
            if "Brakke Grond" in venue.text:
                return "De Brakke Grond", "Nes 45, 1012 KD Amsterdam"
            if "VU Griffioen" in venue.text:
                return "Theater de Griffioen", "De Boelelaan 1111, 1081 HV Amsterdam"
            if "Rhoneweg" in venue.text:
                return "De Sloot", "Rhoneweg 6-10, 1043 AH Amsterdam, Nederland"
            raise Exception('Unhandled case: Frescati op reis, wel in Amsterdam: ' + venue.text)
        return None, None
    location = location.replace(", Amsterdam", "")
    if location == "Theater van Deyssel":
        return "Theater van Deyssel", "Lodewijk van Deysselstraat 91, 1064 HM Amsterdam"
    venue = venue.text.strip()
    if venue == "Frascati 4":
        return "Het Verbond", "Nes 71, 1012 KD Amsterdam"
    if "Frascati" in venue:
        return "Frascati", "Nes 63, 1012 KD Amsterdam"
    if venue in ["Studio 1", "Studio 2", "Studio 3"]:
        return "Frascati", "Nes 63, 1012 KD Amsterdam"
    raise Exception('unknown location: ' + location + ', ' + venue)





def getData(event):
    site = 'https://www.frascatitheater.nl' + event.select_one('.descMetaContainer a.desc').get('href')
    venue, address = formatLocation(event.select_one('.location'), event.select_one('.venue'))
    if not (venue and address):
        return
    return {
        'date': formatDate(event.select_one('.dateTimeInner .datetime .date .start').text.strip()),
        'time': event.select_one('.datetime .time .start').text.strip(),
        'title': formatTitle(event.select_one('h3.title').text.strip(),event.select_one('div.subtitle').text.strip()),
        'venue': venue,
        'price': formatPrice(event.select('tr')),
        'site': site,
        'address': address
    }

def getEventList():
    url = "https://www.frascatitheater.nl/nl/agenda?list_type=events&max=36&page="
    return (event for page in range(1,6) for event in makeSoup(url + str(page)).select('ul.listItems li.eventCard'))

def bot():
    return map(getData, getEventList())
