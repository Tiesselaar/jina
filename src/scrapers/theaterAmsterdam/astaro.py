from src.tools.scraper_tools import myStrptime
from src.tools.scraper_tools import makeSoup
from bs4 import NavigableString, Comment
import re

CALENDARS = ['theaterAmsterdam', 'alternativeAmsterdam']

def singleDateFormat(line, year):
    dateString = " ".join(line.replace(';',':').replace(',','').split())
    dateString += " " + year
    dateFormat = '%A %d %B %H:%M %Y'
    date_time = myStrptime(dateString, dateFormat)
    return {
        'date': date_time.strftime('%Y-%m-%d'),
        'time': date_time.strftime('%H:%M')
    }

def formatDate(lines, year):
    for line in lines:
        try:
            yield singleDateFormat(line, year)
        except Exception as e:
            try:
                words = line.split()
                date1 = singleDateFormat(' '.join(words[:2] + words[-2:]), year)
                date2 = singleDateFormat(' '.join(words[3:]), year)
                yield date1
                yield date2
            except:
                pass


def getData(event_year):
    event, year = event_year
    eventData = {
        'title': event[0],
        'venue': "AstaroTheatro",
        'price': "",
        'site': "https://astarotheatro.com/whats-on/",
        'address': "Sint Jansstraat 37, 1012HG Amsterdam"
    }
    for date_time in formatDate(event, year):
        for calendar in CALENDARS:
            yield {
                **date_time,
                **eventData,
                'calendar': calendar
            }

def lines(tag):
    children = tag.children
    for child in children:
        if child.name == "hr":
            yield child
        elif type(child) == NavigableString:
            text = child.text.strip()
            if text != "":
                yield text
        elif type(child) == Comment:
            continue
        else:
            for line in lines(child):
                yield line

def getEventList():
    url = 'https://astarotheatro.com/whats-on/'
    events = []
    event = []
    running_year = ""
    for line in lines(makeSoup(url).select_one('#content')):
        if type(line) == str:
            if "AstaroTheatro 20" in line:
                running_year = line.split()[1]
                event = []
            else:
                event.append(line)
        else:
            if event:
                events.append([[*event], running_year])
            event = []
    return events


def bot():
    return (gig for event in getEventList() for gig in getData(event))