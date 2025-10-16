from src.tools.scraper_tools import myStrptime, makeSeleniumSoup

# CALENDARS = ['theaterAmsterdam', 'classicalAmsterdam']

def formatDate(date_string):
    dateFormat = '%m/%d/%y, %I:%M %p'
    date = myStrptime(date_string, dateFormat)
    return date.strftime('%Y-%m-%d'), date.strftime('%H:%M')

def formatPrice(price):
    price = price.replace(',-','')
    return price.strip()

def getData(event):
    title_price = event.select_one('.card-heading__content > h4.card-heading__content__title').text
    date, time = formatDate(event.select_one('.card-heading__content .subtitle').text.split(' - ')[0].strip())
    print(date, time)
    standard_format = len(title_price.split('|')) == 4
    print(standard_format)
    return {
        'date': date,
        'time': time,
        'title': title_price.split('|')[1].strip() if standard_format else title_price.strip(),
        'venue': event.select_one('.event-summary-header__location__name').text.strip(),
        'price': formatPrice(title_price.split('|')[3].strip()) if standard_format else "",
        'site': "https://www.comedytrain.nl/tickets/",
        'address': event.select_one('.event-summary-header__location__address').text.strip()
    }

def getEventList():
    url = 'https://shop.weeztix.com/3190150b-4b80-11f0-a9cb-7e126431635e/events'
    events = makeSeleniumSoup(url, 2).select('div[name="events"] > .event-card')
    return events

def bot():
    return map(getData, getEventList())
    # return (gig for event in getEventList() for gig in getData(event))
