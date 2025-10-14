from src.tools.scraper_tools import myStrptime, makeSoup, futureDate

def formatDate(dateString):
    dateString = "".join(dateString.split()[1:]).replace('-Valentijnsspecial','')
    dateString += " 2024"
    dateFormat = '%d/%m %Y'
    date = futureDate(myStrptime(dateString, dateFormat).date(), 60)
    if date.weekday() in range(6):
        time = '19:00'
    if date.weekday() == 6:
        time = '18:30'
    return date.strftime('%Y-%m-%d'), time

def getData(event):
    datestring = " ".join(event.text.split()[:2])
    title = " ".join(event.text.split()[2:])
    date, time = formatDate(datestring)
    eventData = {
        'date': date,
        'time': time,
        'title': title.strip(),
        'venue': "Pompstation",
        'price': "gratis",
        'site': "https://www.pompstation.nu/live-muziek",
        'address': 'Zeeburgerdijk 52, 1094 AE Amsterdam'
    }
    if any([
        'besloten' in title.lower(),
        'geen live muziek' in title.lower()
        ]):
        return
    return eventData

def getEventList():
    venue_name = 'pompstation'
    url = 'https://pompstation.nu/live-muziek'
    events = makeSoup(url).select('ul > li > h4 > button > span')

    return events

def bot():
    return map(getData, getEventList())


