from src.tools.scraper_tools import makeSoup
from bs4 import BeautifulSoup
from html import unescape

from zoneinfo import ZoneInfo
from datetime import datetime


URL = 'https://amsterdamalternative.nl/services/get-events-past-v25.php?&venue=123&months=4'

def find_events(soup: BeautifulSoup):
    import json
    data = json.loads(soup.get_text())
    events = data['items']
    return events

def find_site(event) -> str:
    if event['presale']:
        return event['presale']
    return URL

def find_date(event) -> str:
    return datetime.fromtimestamp(event['start'], tz=ZoneInfo("Europe/Amsterdam")).strftime('%Y-%m-%d')

def find_time(event) -> str:
    return datetime.fromtimestamp(event['start'], tz=ZoneInfo("Europe/Amsterdam")).strftime('%H:%M')

def find_title(event) -> str:
    return unescape(event['title']).strip()

def find_venue(event) -> str:
    return event['venue']

def find_address(event) -> str:
    return 'Sajetplein 39, 1091 DB Amsterdam'

def find_price(event) -> str:
    s = str(event['price']).strip()
    s = s.split()[0]
    s = s.replace(',-', '')
    s = s.replace(',', '.')
    s = ''.join(c for c in s if c.isdigit() or c == '.')
    if s == '':
        return ''
    if s == '0' or s == '0.0' or s == '0.00':
        return 'free'
    return '€' + s

def get_event_data(event):
    return {
        'site': find_site(event),
        'date': find_date(event),
        'time': find_time(event),
        'title': find_title(event),
        'venue': find_venue(event),
        'address': find_address(event),
        'price': find_price(event),
    }

def bot():
    global URL
    soup = makeSoup(URL)
    event_list = find_events(soup)
    return list(map(get_event_data, event_list))