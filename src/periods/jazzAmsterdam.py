__all__= [
    "archiesship",
    # "cecconis",
    "czaar",
    "europe",
    # "groenepaleis",
    "hilton",
    "langereis",
    "meneerdewit",
    "skek",
    "studioK",
    # "vijfnulvijf",
    "zilt"
]

import datetime 

def weekdays(weekday):
    today = datetime.date.today()
    pastSunday = today - datetime.timedelta(days = today.isoweekday())
    return (pastSunday + datetime.timedelta(weeks = week, days = weekday) for week in range(52))

def NthWeekdays(N, weekday):
    def isLast(day):
        return(day.month != (day + datetime.timedelta(weeks = 1)).month)
    return (day for day in weekdays(weekday) if isLast(day - datetime.timedelta(weeks = N)))

## Cafés

def archiesship():
    return map( lambda day:
        {
            'date': day.isoformat(),
            'time': '20:30',
            'title': 'Archie\'s Ship Wednezdayz JazzZezzion',
            'venue': 'Woonschip de \"Zena\"',
            'price': '€10',
            'site': 'https://studiozena.nl/wat-te-doen/muziek/',
            'address': 'Borneokade 68, 1019 AW Amsterdam'
        }, NthWeekdays(2, 3) )

def cecconis():
    # daysList = [*weekdays(4), *weekdays(5), *weekdays(6)]
    daysList = []
    daysList.sort()
    return map( lambda day:
        {
            'date': day.isoformat(),
            'time': '20:00',
            'title': 'Jazz trio',
            'venue': 'Cecconi\'s',
            'price': 'gratis',
            'site': 'https://www.cecconisamsterdam.com/',
            'address': 'Spuistraat 210, 3HG, 1012 VT Amsterdam'
        }, daysList )

def europe():
    daysList = [*weekdays(4), *weekdays(6), *weekdays(7)]
    daysList.sort()
    def get_event_data(day):
        event_data = {
            'date': day.isoformat(),
            'time': {4: '21:00', 6: '15:00', 7: '15:00'}[day.isoweekday()],
            'title': 'Jazz at De L\'Europe',
            'venue': 'Hotel De L\'Europe',
            'price': 'gratis',
            'site': 'https://www.deleurope.com/',
            'address': 'Nieuwe Doelenstraat 2-14, 1012 CP Amsterdam'
        }
        if day.isoweekday() in [6,7]:
            event_data['title'] += ' (solo piano)'
        if day.isoweekday() == 4:
            event_data['venue'] = "Freddy's Bar"
        return event_data
    return map(get_event_data, daysList)
    

def czaar():
    daysList = [*NthWeekdays(2, 6)]
    daysList.sort()
    return map( lambda day:
        {
            'date': day.isoformat(),
            'time': '21:00',
            'title': 'Samuel Kiel et al.',
            'venue': 'Café Czaar',
            'price': 'gratis',
            'site': 'http://czaaramsterdam.nl/',
            'address': 'Czaar Peterstraat 281, 1018 PL Amsterdam'
        }, daysList )

def groenepaleis():
    return map( lambda day:
        {
            'date': day.isoformat(),
            'time': '18:00',
            'title': 'Berend van den Berg, Joost Kesselaar en Erik Robaard',
            'venue': 'Het Groene Paleis',
            'price': 'gratis',
            'site': 'https://hetgroenepaleis.nl/live-muziek/',
            'address': 'Rokin 65, 1012 KK Amsterdam'
        }, weekdays(5) )

def hilton():
    daysList = [*weekdays(5), *weekdays(6), *weekdays(7)]
    daysList.sort()
    return map( lambda day:
        {
            'date': day.isoformat(),
            'time': { 5: '18:00',  6 :'19:00', 7: '16:00' }[day.isoweekday()],
            'title': 'Jazz at the Half Moon Cocktail Lounge',
            'venue': 'Hilton Amsterdam',
            'price': 'gratis',
            'site': 'https://www.hilton.com/en/hotels/amshitw-hilton-amsterdam/',
            'address': '138 Apollolaan, 1077 BG Amsterdam'
        }, daysList )

def langereis():
    return map( lambda day:
        {
            'date': day.isoformat(),
            'time': '20:00',
            'title': 'Gypsy swing session, Tessa Spaaij et al.',
            'venue': 'Caf\u00e9 Langereis',
            'price': 'gratis',
            'site': 'https://cafelangereis.nl/',
            'address': 'Amstel 202, 1017 AH Amsterdam'
        }, NthWeekdays(1,2) )

def meneerdewit():
    daysList = [*weekdays(5), *weekdays(6)]
    daysList.sort()
    return map( lambda day: 
        {
            'date': day.isoformat(),
            'time': '20:30',
            'title': 'Dinner jazz, Maarten Voortman et al.',
            'venue': 'Meneer de Wit Heeft Honger',
            'price': 'gratis',
            'site': 'https://www.meneerdewitheefthonger.nl/',
            'address': 'Witte de Withstraat 10, 1057 XV Amsterdam'
        }, daysList )

# def prael():
#     return map( lambda day: 
#         {
#             'date': day.isoformat(),
#             'time': '18:00',
#             'title': 'Jazzy Sunday',
#             'venue': 'Breugem Meeting Point',
#             'price': 'gratis',
#             'site': 'https://www.breugemmeetingpoint.nl/agenda',
#             'address': 'Nieuwe Hemweg 2, 1013 BG Amsterdam'
#         }, weekdays(7))

def skek():
    return map( lambda day: 
        {
            'date': day.isoformat(),
            'time': '21:30',
            'title': 'Sunday Night Jazz (w/ jam)',
            'venue': '\'SKEK',
            'price': 'gratis',
            'site': 'https://skekamsterdam.cargo.site',
            'address': 'Zeedijk 4-8, 1012 AX Amsterdam'
        }, weekdays(7) )

def studioK():
    return map( lambda day: 
        {
            'date': day.isoformat(),
            'time': '22:00',
            'title': 'Jazz in /K, Felix Schlarmann et al.',
            'venue': 'Studio /K',
            'price': 'gratis',
            'site': 'https://studio-k.nu/events/',
            'address': 'Timorplein 62, 1094 CC Amsterdam'
        }, NthWeekdays(0,3) )

def vijfnulvijf():
    daysList = [*weekdays(3), *weekdays(5)]
    daysList.sort()
    return map( lambda day:
        {
            'date': day.isoformat(),
            'time': '19:00',
            'title': 'Harry Tinney & Alex Ivasenko',
            'venue': 'VIJFNULVIJF',
            'price': 'gratis',
            'site': 'https://www.vijfnulvijf.nl/live-music-bar',
            'address': 'Insulindeweg 505, 1094 MK Amsterdam'
        }, daysList )

def zilt():
    return map( lambda day: 
        {
            'date': day.isoformat(),
            'time': '17:30',
            'title': 'Jasper Blom et al.',
            'venue': 'Café Zilt',
            'price': 'gratis',
            'site': 'https://www.cafezilt.nl/vermaak',
            'address': 'Zeedijk 49, 1012 AR Amsterdam'
        }, NthWeekdays(2,7) )


