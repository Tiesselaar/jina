from src.tools.scraper_tools import myStrptime, makeSoup
import re

CALENDARS = ['popAmsterdam', 'jazzAmsterdam']

def format_date(date_string):
    print(date_string)
    replacements = {
        'Thur': 'Thu',
        'Okt': 'Oct',
        'Zo ': 'Sun ',
        'Sept': 'Sep',
        'Set': 'Sep',
        'Zon ': 'Sun ',
    }
    for old, new in replacements.items():
        date_string = date_string.replace(old, new)
    # if len(date_string) == 10:
    #     date_string += " {}".format(datetime.date.today().year)
    dateFormat = '%a %d %b %Y'
    date = myStrptime(date_string, dateFormat)
    return date.strftime('%Y-%m-%d')

def format_date_time(date_title_string):
    time = re.search(r'\d?\d:\d\d', date_title_string)
    if time:
        time = time[0]
        date_string = date_title_string.split(time)[0].replace(',','').replace('–','').strip()
        title = date_title_string.split(time)[1].strip('– ')
        return format_date(date_string), time, title
    else:
        date_string = " ".join(date_title_string.split()[:4]).replace(',','').replace('–','').strip()
        title = " ".join(date_title_string.split()[4:]).strip('– ')
        return format_date(date_string), None, title

def format_price(price):
    if not price:
        return ""
    price = price.text.strip()
    price = ''.join(price.split())
    return price.replace(',00','')

def getData(event):
    date_title = event.select_one('a h2.woocommerce-loop-product__title').text
    if "Fri 3 & Sat 04 Oct 2025" in date_title:
        return
    if "book: night spaces as" in date_title.lower():
        return
    date, time, title = format_date_time(date_title)
    site = event.select_one('a').get('href')
    if not time:
        subsoup = makeSoup(site, verify=False)
        time = re.search(r'\d?\d:\d\d', subsoup.select_one('h4').text)[0]
    eventData = {
        'date': date,
        'time': time,
        'title': title,
        'venue': "Munganga Theater",
        'price': format_price(event.select_one('a span.price span.woocommerce-Price-amount')),
        'site': site,
        'address': "Schinkelhavenstraat 27 hs, 1075 VP Amsterdam"
    }
    if "jazz" in date_title.lower():
        yield {**eventData, 'calendar': 'jazzAmsterdam'}
    yield {**eventData, 'calendar': 'popAmsterdam'}

def getEventList():
    url = 'https://munganga.nl/'
    events = makeSoup(url, verify=False).select('div.woocommerce ul.products li.product')
    return events

def bot():
    return (gig for event in getEventList() for gig in getData(event))


