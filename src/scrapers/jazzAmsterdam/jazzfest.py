from src.tools.scraper_tools import myStrptime, futureDate, makeSoup

def formatDateTime(date_time_string):
    date_time_vector = date_time_string.split() + ['2024']
    if len(date_time_vector) == 4:
        dateFormat = '%d %b %A %Y'
    elif len(date_time_vector) == 6:
        dateFormat = '%d %b %A %H:%M uur %Y'
    else:
        raise Exception('unknown time format')
    
    date_time_vector[1] = date_time_vector[1][:3] ## kort maand af
    date_time_string = " ".join(date_time_vector)
    date_time = myStrptime(date_time_string, dateFormat)
    date = futureDate(date_time.date())

    if len(date_time_vector) == 4:
        return date.strftime('%Y-%m-%d'), None
    else:
        return date.strftime('%Y-%m-%d'), date_time.strftime('%H:%M')

def formatPrice(price):
    price = price.replace('€ ','€').strip('€').replace(',-','')
    return price.replace('entree', '').replace('v.a.', '').strip()

def getLocation(subsoup):
    try:
        location = subsoup.select_one('a[href^="https://jazzfestamsterdam.nl/locaties/"]')
        return location.text.strip(), makeSoup(location.get('href')).select_one('#main h3').text
    except:
        return "Indische Buurt", "Amsterdam"
    
def get_time(subsoup):
    time_tag = subsoup.select_one('.posts-lists:has(h4:-soup-contains("tijd"))')
    if time_tag:
        return time_tag.select_one('.td-list .td-right').text.split()[0]

    
def getData(event):
    site = event.select_one('a').get('href')
    subsoup = makeSoup(site)

    date_string = event.select_one('.column-text-holder').text
    date, time = formatDateTime(date_string)

    if time == None:
        time = get_time(subsoup)
        if time == None:
            print('no time!')
            return
    
    venue, address = getLocation(subsoup)

    try:
        price = formatPrice(event.select_one('.text-holder-date').text)
    except:
        price = ""
    event_data =  {
        'date': date,
        'time': time,
        'title': event.select_one('.column-text-holder > a > h3').text,
        'venue': venue,
        'price': price,
        'site': site,
        'address': address
    }
    return event_data


def getEventList():
    venue_name = 'jazzfest'
    url = 'https://jazzfestamsterdam.nl/agenda/'
    events = makeSoup(url).select('#evenementen .event-grid-cont')
    return events

def bot():
    return map(getData, getEventList())