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

def getData(event):
    event_date, event_time = formatDate(event.select_one('.d-when').text)
    return {
        'date': event_date,
        'time': event_time,
        'title': event.select_one('.d-title').text.strip(),
        'venue': "Kaskantine",
        'price': "",
        'site': "https://tockify.com" + event.select_one('.d-title a').get('href'),
        'address': "Handbalstraat 1, 1062 XA Amsterdam, Nederland"
    }
    
def getEventList():
    url = 'https://tockify.com/kaskantine/agenda'
    scripts = ["button = document.querySelector(\"a[translate='loadMoreEvents']\"); if (button) {button.click()};"]
    events = makeSeleniumSoup(url, 1, scripts= 3 * scripts).select('.agenda .agendaItem')
    return events

def bot():
    return map(getData, getEventList())