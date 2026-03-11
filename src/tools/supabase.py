import os
from supabase import create_client, Client
import datetime
from dotenv import load_dotenv
load_dotenv()
import re

def server():
    url: str = os.environ.get("SUPABASE_URL")
    key: str = os.environ.get("SUPABASE_KEY")
    supabase: Client = create_client(url, key)
    return supabase

def format_price(price):
    price = price.replace(',','.')
    price = re.sub(r'\.00\b', '', price)
    price = re.sub(r'\.([1-9])0\b', r'.\1', price)
    price = re.sub(r'[gG]ratis', 'free', price)
    return price.strip()

def update_record(calendar, venue, gigs):
    today = (datetime.date.today()).isoformat()
    gigs = [gig for gig in gigs if gig['date'] >= today]
    for gig in gigs:
        gig['calendar'] = calendar
        gig['source'] = venue
        gig['price'] = format_price(gig['price'])

    supabase = server()
    supabase.table('gigs').delete().eq('calendar', calendar).eq('source', venue).gte('date', today).execute()
    if gigs == []:
        return 0
    response = supabase.table('gigs').upsert(gigs, count='exact').execute()
    return response.data