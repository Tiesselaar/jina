from src.tools.scraper_tools import myStrptime
from src.tools.scraper_tools import makeSoup, futureDate

# CALENDARS = ['theaterAmsterdam', 'classicalAmsterdam']

def formatDate(dateString):
    dateString = dateString.replace('vanaf', '').replace('|', ' ').replace(',', '')
    datestring = " ".join(dateString.split())
    dateString += " 2024"
    dateFormat = '%A %d %B %H:%M %Y'
    date = myStrptime(dateString, dateFormat)
    time = date.strftime('%H:%M')
    date = futureDate(date.date(), 60)
    return date.strftime('%Y-%m-%d'), time

def getData(event):
    dateString = [div for div in event.select('div p span span span') if '| vanaf' in div.text][0].text
    date, time = formatDate(dateString)
    return {
        'date': date,
        'time': time,
        'title': " ".join(event.select_one(':scope > div > h2').text.split()),
        'venue': "Hulscher's",
        'price': "",
        'site': "https://www.hulschers.com/nl",
        'address': "Nieuwezijds Voorburgwal 176-180, 1012 SJ Amsterdam"
    }

def getEventList():
    url = 'https://www.hulschers.com/nl'
    divs = makeSoup(url).select('div > [data-testid="inline-content"] > [data-testid="mesh-container-content"]')
    def testDiv(div):
        header = div.select_one(':scope > div > h2')
        if header:
            return "jazz" in header.text.strip().lower()
    return [div for div in divs if testDiv(div)]
    
def bot():
    return map(getData, getEventList())
    # return (gig for event in getEventList() for gig in getData(event))
