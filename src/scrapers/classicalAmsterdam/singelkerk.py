from src.tools.scraper_tools import myStrptime
from src.tools.scraper_tools import makeSoup, futureDate

def formatDate(dateString):
    dateFormat = '%d/%m/%Y'
    date = myStrptime(dateString, dateFormat).date()
    return date.strftime('%Y-%m-%d')

def formatAddress(address):
    lines = [line.strip() for line in address.split('\n')]
    lines = [line for line in lines if line!='' and line!='Adres']
    return ', '.join(lines)


def getData(event):
    if any(keyword in event.text.lower() for keyword in ["concert", "klassiek", "kamerkoor"]):
        site = event.select_one('.eventinfo h3 a').get('href')
        try:
            location_link = makeSoup(site).select_one('a[href^="https://www.doopsgezindamsterdam.nl/locations"]').get('href')
        except Exception as e:
            if "Oudezijds 100" in event.text:
                return
            else:
                raise e
        location_page = makeSoup(location_link)
        return {
            'date': formatDate(event.select_one('td.datetime strong').text.split(' - ')[0]),
            'time': event.select_one('td.datetime').contents[-1].split()[0],
            'title': event.select_one('.eventinfo h3 a').text,
            'venue': location_page.select_one('article.location h2.blog-single-title[itemprop="headline"]').text,
            'price': "",
            'site': site,
            'address': formatAddress(location_page.select_one('div[data-view="location"] > div > p').text),
        }

def getEventList():
    url = 'https://www.doopsgezindamsterdam.nl/programma/?pno='
    events = sum((makeSoup(url + str(page)).select('table.events-table > tbody > tr') for page in range(1, 5)), [])
    return events

def bot():
    return map(getData, getEventList())
