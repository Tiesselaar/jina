from src.tools.scraper_tools import myStrptime, makeSeleniumSoup
import datetime

def formatDate(dateTimeString):
    dateTimeTuple = dateTimeString.split('-')[0].split()
    for suffix in ["th", "st", "nd", "rd"]:
        dateTimeTuple[1] = dateTimeTuple[1].replace(suffix, '')
    if len(dateTimeTuple) == 4:
        dateTimeTuple.insert(3, str(datetime.date.today().year))
    dateTimeString = " ".join(dateTimeTuple).replace('.', '')
    dateFormat = '%a %d %b %Y %H:%M'
    dateTime = myStrptime(dateTimeString, dateFormat)
    return dateTime.strftime('%Y-%m-%d'), dateTime.strftime('%H:%M')

def formatTitle(title):
    if "JAZZ" in title:
        return title.title()
    return title

def getData(event):
    title = formatTitle(event.select_one('.d-title').text.strip())
    if "gesloten" in title.lower() or "closed" in title.lower():
        return
    if 'sketch jam' in event.select_one('.d-text').text.lower() + event.select_one('.d-title').text.lower():
        return
    event_date, event_time = formatDate(event.select_one('.d-when').text)
    return {
        'date': event_date,
        'time': event_time,
        'title': title,
        'venue': "Café de Pianist",
        'price': "gratis",
        'site': "https://www.cafedepianist.nl/agenda-live-muziek/",
        'address': 'Groen van Prinstererstraat 41, 1051 EH Amsterdam'
    }
    
def getEventList():
    url = 'https://tockify.com/cafedepianist.nl/agenda'
    scripts = ["document.querySelector(\"a[translate='loadMoreEvents']\").click();"]
    events = makeSeleniumSoup(url, 1, scripts= 5 * scripts).select('.agenda .agendaItem')
    return events

def bot():
    return map(getData, getEventList())