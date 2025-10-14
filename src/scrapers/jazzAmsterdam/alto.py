from src.tools.scraper_tools import makeSoup, myStrptime

def formatDate(date):
    dateFormat = '%a%d%b%Y'
    my_date = myStrptime(date, dateFormat)
    return my_date.strftime('%Y-%m-%d')

def dateToPrice(gig_date, gig_time):
    gig_isoweekday = myStrptime(gig_date, '%Y-%m-%d').isoweekday()
    if gig_isoweekday in [1,2,3,4,7] and gig_time == '21:00':
        return '€5'
    elif gig_isoweekday in [5,6] and gig_time == '21:00':
        return '€10'
    else:
        return ''
    
def dateToTime(gig_date):
    gig_isoweekday = myStrptime(gig_date, '%Y-%m-%d').isoweekday()
    if gig_isoweekday in [1,2,3,4,5]:
        return "20:30"
    return "21:00"

def getData(event):
    date = formatDate(event.select_one('.start-date').text)
    title = event.select_one('.event-title a').text
    print(title)
    time = event.select_one('.event-time')
    if time:
        time = time.text.split('-')[0].replace('.',':')
    else:
        time = dateToTime(date)
    eventData = {
        'date': date,
        'time': time,
        'title': title,
        'venue': "Jazz Café Alto",
        'price': dateToPrice(date, time),
        'site': event.select_one('.event-title a').get('href'),
        'address': "Korte Leidsedwarsstraat 115, 1017 PX Amsterdam"
    }
    if eventData["title"] == "Bop This":
        eventData["title"] += "!"
    return eventData

def getEventList():
    url='https://www.jazz-cafe-alto.nl'
    events = makeSoup(url).select('.event')
    return events

def bot():
    return map(getData, getEventList())