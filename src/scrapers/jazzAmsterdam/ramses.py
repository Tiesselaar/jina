from src.tools.scraper_tools import myStrptime, makeSoup, makeSeleniumSoup
import re

def formatDateTime(dateTime):
    timeSearch = re.search(r"\d?\d:\d\d", dateTime)
    if timeSearch:
        time = timeSearch[0]
    else:
        time = None
    dateString = " ".join(dateTime.split()[:4]).replace(',', '').replace('middag','')
    if "vanaf" in dateString.lower():
        date = None
    else:
        dateFormat = '%A %d %B %Y'
        date = myStrptime(dateString, dateFormat).strftime('%Y-%m-%d')
    return date, time

def formatPrice(eventText):
    eventText = " ".join(eventText.split())
    priceSearch = re.search(r"(€) ?\d+([,.]\d+|,=|,-)?", eventText.split("Entree: ")[-1].split('\n')[0])
    if priceSearch:
        return priceSearch[0].replace(' ','').replace(',=','').replace(',-','').replace(',00','')
    priceSearch = re.search(r"Entree: ?\d+([,.]\d+|,=|,-)?", eventText)
    if priceSearch:
        return priceSearch[0].replace('Entree:', '€').replace(' ','').replace(',=','').replace(',-','').replace(',00','')
    return ""

def getData(event):
    site = event.select_one('a').get('href')
    print(site)
    subsoup = makeSoup(site)

    if "jazz" in subsoup.select_one('#main .entry-content').text.lower():
        try:
            eventDate, eventTime = formatDateTime(subsoup.select_one('div > div > div.vc_row.wpb_row.vc_row-fluid.vc_column-gap-25 > div.wpb_column.vc_column_container.vc_col-sm-8 > div > div > h5').text)
        except:
            try:
                eventDate, eventTime = formatDateTime(subsoup.select_one('.wpb-content-wrapper .wpb_wrapper > h3').text)
            except:
                try:
                    eventDate, eventTime = formatDateTime(subsoup.select_one('.wpb-content-wrapper .wpb_wrapper > h3 > span').text)
                except:
                    try:
                        eventDate, eventTime = formatDateTime(subsoup.select('.wpb-content-wrapper .wpb_wrapper > h2')[1].text)
                    except:
                        print('Date failed:')
                        print(site)
                        return

        if eventDate and eventTime:
            subtitleElement = subsoup.select_one('.wpb-content-wrapper h1')
            subtitle = " | " + subtitleElement.text if subtitleElement else ""
            eventData = {
                'date': eventDate,
                'time': eventTime,
                'title': subsoup.select_one('.wpb-content-wrapper h2').text + subtitle,
                'venue': "Sociëteit Ramses Shaffy Huis",
                'price': formatPrice(subsoup.select_one('#main').text),
                'site': site,
                'address': "Piet Heinkade 231, 1019 HM Amsterdam"
            }
            return eventData

def getEventList():
    url = 'https://kunstenaarshuizen.amsterdam/culturele-agenda-verwacht/'
    events = makeSeleniumSoup(url, 2).select('.vc_grid .vc_pageable-slide-wrapper .vc_grid-item')
    return events

def bot():
    from concurrent.futures import ThreadPoolExecutor
    with ThreadPoolExecutor() as executor:
        results = list(executor.map(getData, getEventList()))
    return results
