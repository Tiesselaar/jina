from src.tools.scraper_tools import myStrptime, makeSoup, makeSeleniumSoup, futureDate

def formatDate(date):
    dateType = len(date.split())
    if dateType == 2:
        pass
    elif dateType == 4:
        date = date.split()[0] + " " + date.split()[-1]
    else:
        raise Exception("Event over multiple months not implemented")

    dateFormat = '%d %B %Y'
    dateThisYear = date + " 2020"
    date = futureDate(myStrptime(dateThisYear, dateFormat).date())
    return date.strftime('%Y-%m-%d')

def formatPrice(priceTag):
    if priceTag:
        return "".join(priceTag.text.split()).replace('.',',')
    return ""

def getData(event):
    eventTitle = event.select_one('.mec-event-content h4.mec-event-title a.mec-color-hover').text
    if "blues" in eventTitle.lower() or "jazz" in eventTitle.lower():
        site = event.select_one('.mec-event-content h4.mec-event-title a.mec-color-hover').get('href')
        print(site)
        subsoup = makeSeleniumSoup(site, 4)

        eventData = {
            'date': formatDate(event.select_one('.event-grid-t2-head .mec-event-month span[itemprop="startDate"]').text),
            'time': event.select_one('.event-grid-t2-head .mec-time-details span.mec-start-time').text,
            'title': eventTitle,
            'venue': "Het Sieraad",
            'price': formatPrice(subsoup.select_one('.price > h2.amount')),
            'site': site,
            'address': "Postjesweg 1, 1057 DT Amsterdam"
        }
        return eventData


def getEventList():
    venue_name = 'sieraad'
    url = 'https://www.het-sieraad.nl/agenda/'
    events = makeSoup(url).select('.mec-event-grid-clean article.mec-event-article')
    return events

def bot():
    return map(getData, getEventList())


