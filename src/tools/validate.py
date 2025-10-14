import re

def venue(venue_string):
    if type(venue_string) == str and venue_string:
        return
    raise Exception("invalid venue: " + venue_string)

def title(title_string):
    if type(title_string) == str and title_string:
        return
    raise Exception("invalid title: " + title_string)

def time(time_string):
    if type(time_string) == str:
        if re.match(r'\d\d:\d\d$', time_string):
            if int(time_string[:2]) < 24 and int(time_string[-2:]) < 60:
                return
    raise Exception("invalid time: " + time_string)

def date(date_string):
    if type(date_string) == str:
        if re.match(r'\d\d\d\d-\d\d-\d\d$', date_string):
            return
    raise Exception("invalid date: " + date_string)

def site(url):
    if type(url) == str:
        if re.search(r'https?://', url):
            return
    raise Exception("invalid site: " + url)

def price(price_string):
    if type(price_string) == str:
        return
    raise Exception("invalid price: " + price_string)

def gig(gig_object):
    title(gig_object['title'])
    venue(gig_object['venue'])
    date(gig_object['date'])
    time(gig_object['time'])
    site(gig_object['site'])
    price(gig_object['price'])

def check_order(gig_list):
    if (
        gig_list[0]['date'] + 'T' + gig_list[0]['time'] <=
        gig_list[1]['date'] + 'T' + gig_list[1]['time']
    ):
        return
    raise Exception('gigs not in order')

def gigs(gig_list):
    list(map(gig, gig_list))
    # list(map(check_order, zip(gig_list[:-1], gig_list[1:])))