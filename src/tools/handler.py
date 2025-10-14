from src import scrapers, periods
from src.tools import validate, supabase
import json

def get_gigs(calendar, venue, noval):
    venue_module = getattr(getattr(scrapers, calendar), venue)
    gigs = [x for x in venue_module.bot() if x]
    if not noval:
        validate.gigs(gigs)
    try:
        calendars = venue_module.CALENDARS
        return {
            cal: [gig for gig in gigs if gig['calendar'] == cal]
            for cal in calendars
        }
    except:
        return {calendar: gigs}

def get_period(calendar, venue):
    gigs = list(getattr(getattr(periods, calendar), venue)())
    validate.gigs(gigs)
    return {calendar: gigs}

def format_count(gigs):
    if all(gigs[cal] == 0 for cal in gigs):
        return 0
    if len(gigs) == 1:
        return len(list(gigs.values())[0])
    for cal in gigs:
        if gigs[cal] == 0:
            gigs[cal] = []
    return ", ".join(f"{cal[:2]}: {len(gigs[cal])}" for cal in gigs)

def update_agenda(calendar, venue, debug, noval):
    if (
        calendar in periods.__all__ and
        venue in getattr(periods, calendar).__all__
    ):
        gigs = get_period(calendar, venue)
    else:
        gigs = get_gigs(calendar, venue, noval)
    if debug:
        print(json.dumps(gigs, indent=2))
        return format_count(gigs)
    if noval:
        ## this is obsolete
        return
    data = {cal: supabase.update_record(cal, venue, gigs[cal]) for cal in gigs}
    return format_count(data)