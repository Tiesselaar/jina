from src.tools.scraper_tools import makeSoup
import requests
import json
import datetime
from html import unescape

CALENDARS = ['religionAmsterdam', 'classicalAmsterdam']


def format_address(location):
    if "Dominicus" in location or location == '':
        return "Spuistraat 12A, 1012 TS Amsterdam"
    elif location == "Extern":
        return None
    else:
        raise Exception("unknown location: " + location)
    
def getData(event):
    address = format_address(event['location'])
    if not address:
        return
    event_data = {
        'date': event['start_date'].split()[0],
        'time': event['start_date'].split()[1][:5],
        'title': unescape(event['title']),
        'venue': "Dominicuskerk",
        'price': "",
        'site': event['url'],
        'address': address
    }
    yield {**event_data, 'calendar': 'religionAmsterdam'}
    keywords = ['muziek', 'music', 'concert', 'orkest', 'koor']
    if any(keyword in event['description'].lower() for keyword in keywords):
        yield {**event_data, 'calendar': 'classicalAmsterdam'}



def get_events_for_month(month, year, nonce):
    api = "https://dominicusamsterdam.nl/wp-admin/admin-ajax.php"
    payload = {
        "action": "get_dom_events_for_month",
        "nonce": nonce,
        "year": year,
        "month": month,
    }
    response = requests.post(api, data=payload)
    days = json.loads(response.text)['data']
    return list(sum([days[day] for day in days], []))

def getEventList():
    this_year = datetime.datetime.today().year
    this_month = datetime.datetime.today().month
    months = [(this_month + x - 1 ) % 12 + 1 for x in range(4)]
    years = [this_year + int((this_month + x - 1 ) / 12) for x in range(4)]
    month_years = zip(months, years)

    soup = makeSoup("https://dominicusamsterdam.nl/agenda/")
    nonce = soup.select_one('.dom-calendar-container').get('data-nonce')

    return [event for month, year in month_years for event in get_events_for_month(month, year, nonce)]

def bot():
    return (gig for event in getEventList() for gig in getData(event))
