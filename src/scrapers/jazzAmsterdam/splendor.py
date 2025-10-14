from src.tools.scraper_tools import myStrptime, makeSoup

def formatDateTime(dateTimeString):
    dateFormat = '%A %d %b %Y - %H:%M uur'
    date = myStrptime(dateTimeString.replace('.', '').strip(), dateFormat)
    return date.strftime('%Y-%m-%d'), date.strftime('%H:%M')

def formatPrice(tickets):
    for ticket in tickets:
        if ticket.select('.type')[0].text == "Ticket":
            return ticket.select('.price')[0].text.replace('.',',')
    return ""

def getData(event):
    description = event.text.lower()
    if 'jazz' in description or 'improv' in description:
        date, time = formatDateTime(event.select_one('li.date').text)
        eventData = {
            'date': date,
            'time': time,
            'title': event.select_one('li h1').text + " - " + event.select_one('li h2').text,
            'venue': "Splendor",
            'price': formatPrice(event.select('li .ticket')),
            'site': event.select_one(':scope > li > a[href*="splendoramsterdam.com/agenda"]').get('href'),
            'address': 'Nieuwe Uilenburgerstraat 116, 1011 LX Amsterdam'
        }
        if "dit concert vindt plaats in de uilenburgersjoel" in description:
            eventData['venue'] = "Uilenburgersjoel"
            eventData['address'] = "Nieuwe Uilenburgerstraat 91, 1011 LM Amsterdam"
        return eventData


def getEventList():
    venue = 'splendor'
    url='https://splendoramsterdam.com/agenda/feed'
    events = makeSoup(url).select('body > div > ul')
    return events

def bot():
    return map(getData, getEventList())

