from src.tools.scraper_tools import makeSoup, makeSeleniumSoup
from bs4 import BeautifulSoup

URL = 'https://desering.org/events'

def find_events(soup: BeautifulSoup):
    return soup.select('a[href^="/event/"]')

def find_site(event) -> str:
    href = event['href']
    if href.startswith('http'):
        return href
    return 'https://desering.org' + href

def find_date(event) -> str:
    return event.select_one('time')['datetime'][:10]

def find_time(event) -> str:
    from datetime import datetime
    from zoneinfo import ZoneInfo
    dt_str = event.select('time')[0]['datetime']
    dt = datetime.fromisoformat(dt_str.replace('Z', '+00:00'))
    local = dt.astimezone(ZoneInfo('Europe/Amsterdam'))
    return local.strftime('%H:%M')

def find_title(event) -> str:
    return event.select_one('div.c1jwpogg').get_text(strip=True)

def find_venue(event) -> str:
    return "De Sering"

def find_address(event) -> str:
    return "Rhôneweg 6, 1043 AH Amsterdam"

def find_price(event) -> str:
    return ""

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