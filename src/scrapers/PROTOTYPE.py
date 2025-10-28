from src.tools.scraper_tools import myStrptime, makeSoup #, futureDate

# CALENDARS = ['theaterAmsterdam', 'classicalAmsterdam']

def formatDate(dateString):
    # dateString += " 2024"
    dateFormat = '%a %d %B %Y'
    date = myStrptime(dateString, dateFormat).date()
    # date = futureDate(date)
    return date.strftime('%Y-%m-%d')

# def formatTime(time):
#     # format time as '21:00'
#     return time

# def formatPrice(price):
#     # format price as '\u20ac12,50' (no space!)
#     price = price.replace(' ','')
#     return price

def getData(event):
    site = event.select_one('a').get('href')
    # subsoup = makeSoup(site)
    return {
        'date': formatDate(event.select_one('').text),
        'time': event.select_one('').text,
        'title': event.select_one('').text,
        'venue': "",
        'price': "",
        'site': site,
        'address': ""
    }

def getEventList():
    url = ''
    events = makeSoup(url).select('')
    return events

def bot():
    return map(getData, getEventList())

# def bot():
    # return (gig for event in getEventList() for gig in getData(event))


# def bot():
#     from concurrent.futures import ThreadPoolExecutor
#     with ThreadPoolExecutor() as executor:
#         results = list(executor.map(getData, getEventList()))
#     return results


# def bot():
#     from concurrent.futures import ThreadPoolExecutor
#     with ThreadPoolExecutor() as executor:
#         return (
#             gig
#             for gigs in executor.map(lambda event: list(getData(event)), getEventList())
#             for gig in gigs
#         )