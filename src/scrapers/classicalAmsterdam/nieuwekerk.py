from src.tools.scraper_tools import myStrptime
from src.tools.scraper_tools import makeSoup, futureDate

def formatDate(dateString):
    dateFormat = '%d %B %Y'
    date = myStrptime(dateString, dateFormat).date()
    return date.strftime('%Y-%m-%d')

def getData(event):
    site = event.select_one('a').get('href')
    subsoup = makeSoup(site)
    return {
        'date': formatDate(subsoup.select_one('section.content > h2 + aside > span').text.strip(),),
        'time': event.select('.activiteit-tijden span')[1].text.split()[0],
        'title': event.select_one('.activiteit-info > h4').text,
        'venue': "De Nieuwe Kerk",
        'price': subsoup.select_one('.sidebar-item.pricetag table tr').select('td')[-1].text.replace(" ", ""),
        'site': site,
        'address': "De Dam, 1012 NL Amsterdam"
    }

def getEventList():
    url = 'https://www.nieuwekerk.nl/agenda/'
    events = makeSoup(url).select('ul.agenda-list li:is(.orgelconcert,.concert)')
    return events

def bot():
    return map(getData, getEventList())
