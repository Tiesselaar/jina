CALENDARS = ['popAmsterdam', 'jazzAmsterdam']

import requests

URL = "https://knwxh8dmh1.execute-api.eu-central-1.amazonaws.com/graphql"

payload = {
    "query": """
    {
      program(site:"paradisoNederlands", size:500) {
        events {
          uri
          title
          subtitle
          startDateTime
          eventStatus
          supportAct
          soldOut
          location {
            title
          }
        }
      }
    }
    """
}

VENUES = {
  "Paradiso": "Weteringschans 6-8, 1017 SG Amsterdam, NL",
  "Tolhuistuin": "IJpromenade 2, 1031 KT Amsterdam, NL",
  "Zonnehuis": "Zonneplein 30, 1033 EK Amsterdam, NL",
  "Bitterzoet": "Spuistraat 2, 1012 TS Amsterdam, NL",
  "Parallel": "Kijkduinstraat 3, 1055 XP Amsterdam, NL",
  "Academie voor Theater en Dans": "Jodenbreestraat 3, 1011 NG Amsterdam, NL",
  "Cinetol": "Tolstraat 182, 1074 VM Amsterdam, NL",
  "AFAS Live": "Johan Cruijff Boulevard 590, 1101 DS Amsterdam, NL",
  "Toekomstmuziek": "Danzigerbocht 29, 1013 AM Amsterdam",
  "De Duif": "Prinsengracht 756, 1017 LD Amsterdam",
}


def getData(event):
    venue = event['location'][0]['title'] if event['location'] else "Paradiso"
    event_data = {
        'date': event['startDateTime'].split('T')[0],
        'time': event['startDateTime'].split('T')[1][:5],
        'title': event['title'] + \
          (" + " + event['supportAct'] if event['supportAct'] else "") + \
          (" (sold out)" if event['soldOut'] == 'yes' else "") + \
          (" (CANCELLED)" if event['eventStatus'] == 'canceled' else "") + \
          (" (POSTPONED)" if event['eventStatus'] == 'postponed' else ""),
        'venue': venue,
        'price': "",
        'site': "https://www.paradiso.nl/" + event['uri'],
        'address': VENUES[venue]
    }
    yield {'calendar': 'popAmsterdam', **event_data}
    if 'jazz' in (event['subtitle'] or '' + event['title'] or '' + event['supportAct'] or '').lower():
      yield {'calendar': 'jazzAmsterdam', **event_data}

def getEventList():
    return requests.post(URL, json=payload).json()['data']['program']['events']


def bot():
    from concurrent.futures import ThreadPoolExecutor
    with ThreadPoolExecutor() as executor:
        return (
            gig
            for gigs in executor.map(lambda event: list(getData(event)), getEventList())
            for gig in gigs
        )
