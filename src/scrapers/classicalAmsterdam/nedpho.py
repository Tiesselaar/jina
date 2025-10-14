from src.tools.scraper_tools import myStrptime, makeSoup #, futureDate

# CALENDARS = ['theaterAmsterdam', 'classicalAmsterdam']

def formatDate(dateString):
    # dateString += " 2024"
    dateFormat = '%a. %d %B %Y'
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
    site = 'https://orkest.nl' + event.select_one('a').get('href')
    # subsoup = makeSoup(site)
    return {
        'date': formatDate(event.select_one('.card-wide__date-time span').text),
        'time': event.select('.card-wide__date-time span')[1].text.strip(),
        'title': event.select_one('h3.card-wide__title').text,
        'venue': "NedPhO-Koepel",
        'price': "",
        'site': site,
        'address': "Batjanstraat 3, 1094 RB Amsterdam"
    }

def getEventList():
    url = 'https://orkest.nl/concerten/?location=nedpho-koepel'
    events = makeSoup(url).select('#main .card-list li.card-list__list-item')
    return events

def bot():
    return map(getData, getEventList())
    # return (gig for event in getEventList() for gig in getData(event))