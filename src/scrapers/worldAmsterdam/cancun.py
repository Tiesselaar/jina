from src.tools.scraper_tools import makeSoup
from bs4 import BeautifulSoup

URL = 'https://cancunamsterdam.nl/agenda/'

def find_events(soup: BeautifulSoup):
    return soup.select('.elementor-loop-container .e-loop-item')

def find_site(event) -> str:
    return "https://cancunamsterdam.nl/agenda/"

def find_date(event) -> str:
    import datetime, re
    t = event.select('h2.premium-dual-header-first-header span.premium-dual-header-first-span')[0].get_text(" ", strip=True)
    m = re.search(r'(\d{1,2})\s*([A-Za-z]{3})', t)
    day = int(m.group(1))
    mon = m.group(2).title()
    months = {'Jan':1,'Feb':2,'Mar':3,'Apr':4,'May':5,'Jun':6,'Jul':7,'Aug':8,'Sep':9,'Oct':10,'Nov':11,'Dec':12}
    month = months[mon]
    today = datetime.date.today()
    year = today.year
    d = datetime.date(year, month, day)
    if d < today:
        d = datetime.date(year + 1, month, day)
    return d.strftime('%Y-%m-%d')

def find_time(event) -> str:
    h2 = event.select('h2.premium-dual-header-first-header')
    if not h2:
        return "17:00"
    spans = h2[0].select('span')
    if len(spans) < 2:
        return "17:00"
    t = spans[1].get_text(strip=True)
    if '–' in t:
        return t.split('–')[0].strip()
    if '-' in t:
        return t.split('-')[0].strip()
    if ':' in t:
        return t.strip()
    return "17:00"

def find_title(event) -> str:
    return event.select('.premium-dual-header-first-span')[-1].get_text(strip=True)

def find_venue(event) -> str:
    return "Cancún"

def find_address(event) -> str:
    return "Veelaan 15, 1019 AP, Amsterdam"

def find_price(event) -> str:
    text = event.get_text(" ", strip=True)
    if "free" in text.lower():
        return "free"
    import re
    m = re.search(r"€\s*([\d]+(?:[.,]\d{1,2})?)", text)
    if m:
        return m.group(1).replace(",", ".")
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