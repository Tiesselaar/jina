#!/usr/bin/env python3
from concurrent.futures import ThreadPoolExecutor
from src.tools import handler, mailjet
from settings import shortcuts, MAX_WORKERS

import time
import sys
from dotenv import load_dotenv
load_dotenv()

def email(message):
    mailjet.mail(
        'Content',
        'JinaBot',
        f"""
<pre>{message}

https://jazzin.amsterdam
</pre>
""")

LOGFILE = "./log.txt"

def print_log(message, method='a', end="\n"):
    log_file = open(LOGFILE, method)
    log_file.write(message + end)
    log_file.close()
    print(message + "\n")

def try_update_agenda(args):
    venue, calendar, debug, noval = args
    try:
        start = time.time()
        count = handler.update_agenda(calendar, venue, debug, noval)
        elapsed_time = int(time.time() - start)
        print(f"Done: {calendar}, {venue}")
        return {
            "calendar": calendar,
            "venue": venue,
            "status": "passed",          
            "count": count,
            "elapsed_time": elapsed_time
            }
    except Exception as e:
        if debug:
            raise e
        return {
            "calendar": calendar,
            "venue": venue,
            "status": "failed",
            "error": str(e)
            }
    
# def get(venues, debug, noval):
#     for calendar in venues:
#         with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
#             results = executor.map(try_update_agenda, [
#                 (venue,
#                 calendar,
#                 debug,
#                 noval) for venue in venues[calendar]
#                 ])
    
#         print_log("\n ---- {} ----".format(calendar))
#         for result in results:
#             print_log(result['venue'].ljust(20), end="")
#             if result['status'] == 'passed':
#                 print_log(f"{result['count'] and ' ' or 'empty'}")
#                 print(f"Count: {result['count']}")
#                 print(f"https://jazzin.amsterdam/cal/{result['calendar']}/venues/{result['venue']}")
#             else:
#                 print_log(result['error'].splitlines()[0])
#             print("")
#             print("-" * 80 * 2, end="\n\n")

def get(venues, debug, noval):
    for calendar in venues:
        print_log("\n ---- {} ----".format(calendar))
        for venue in venues[calendar]:
            print_log(venue.ljust(20), end="")
            try:
                count = handler.update_agenda(calendar, venue, debug, noval)
                print_log(f"passed ({count})".ljust(15) + ("empty set!" if count == 0 else ""))
                print(f"https://jina3.vercel.app/cal/{calendar}/venues/{venue}")
            except Exception as e:
                if debug:
                    raise e
                print_log("⚠⚠⚠ exception".ljust(15) + str(e))
            print("")
            print("-" * 80 * 2, end="\n\n")

all_venues = {
    calendar: [venue for venue in getattr(handler.scrapers, calendar).__all__]
    for calendar in handler.scrapers.__all__
}

all_periods = {
    calendar: [venue for venue in getattr(handler.periods, calendar).__all__]
    for calendar in handler.periods.__all__
}

if __name__=="__main__":
    print("\n" + ("#" * 80) * 2, end="")
    print_log("", 'w', end="")
    args = sys.argv[1:]
    
    debug = bool(args.count('--debug')) and bool(args.pop(args.index('--debug')))
    noval = False
    if debug:
        noval = bool(args.count('--noval')) and bool(args.pop(args.index('--noval')))
    mail = bool(args.count('--mail')) and bool(args.pop(args.index('--mail')))

    if len(args) == 0:
        venues = all_venues
    elif len(args) == 1 and args[0] == "--periods":
        venues = all_periods
    else:
        for shortcut in shortcuts:
            if args[0] == shortcut:
                args[0] = shortcuts[shortcut]
        if len(args) == 1:
            venues = { args[0]: all_venues[args[0]] }
        elif len(args) == 2:
            venues = { args[0]: [args[1]] }
        else:
            print_log("WRONG NUMBER OF ARGUMENTS")
            venues = {}
    
    get(venues, debug, noval)

    log_file = open(LOGFILE, 'r')
    print("SUMMARY:\n")
    log_string = log_file.read()
    print(log_string)
    if mail: email(log_string)
    log_file.close()