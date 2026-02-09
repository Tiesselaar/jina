from src.tools.scraper_tools import myStrptime
from src.tools.scraper_tools import makeSoup, futureDate
import re

def formatDate(dateString):
    # dateString += " 2024"
    dateFormat = '%d %B %Y'
    date = myStrptime(dateString, dateFormat).date()
    # date = futureDate(date)
    return date.strftime('%Y-%m-%d')

def formatTime(global_info):
    time_pattern = r'Er worden concerten uitgevoerd op onderstaande zondagochtenden om \d\d.\d\d uur'
    time_search = re.search(time_pattern, global_info)[0]
    return time_search.split()[-2].replace('.',':')

def formatPrice(global_info):
    global_info = " ".join(global_info.split())
    price_pattern = r'regulier € \d+(,\d\d)?'
    price_search = re.search(price_pattern, global_info)[0]
    return "€" + str(float(price_search.split()[-1].replace(',','.')))

def getData(event, global_time, global_price):
    date_time = event.select_one('a.ut-blog-link .entry-content p').text
    return {
        'date': formatDate(date_time.split(' aanvang ')[0]),
        'time': date_time.split(' aanvang ')[1].split()[0],
        'title': event.select_one('header.entry-header h2.entry-title').text,
        'venue': "Kamermuziek in de Koningszaal",
        'price': global_price,
        'site': event.select_one('a.ut-blog-link').get('href'),
        'address': "Plantage Middenlaan 41-A, 1018 DC  Amsterdam"
    }

def getEventList():
    url = 'https://kamukoza.nl/aankomende-concerten/'
    events = makeSoup(url).select_one('.ut-blog-grid-module').select('.ut-blog-grid-article')
    return events

def bot():
    global_info = makeSoup('https://kamukoza.nl').text
    global_time = formatTime(global_info)
    global_price = formatPrice(global_info)

    return map(lambda event: getData(event, global_time, global_price), getEventList())
