import requests

cinemas = [
    {
        'tag': 'pathe-de-munt',
        'name': 'Pathé de Munt',
        'address': 'Vijzelstraat 15, 1017 HD Amsterdam',
    },
    {
        'tag': 'koninklijk-theater-tuschinski',
        'name': 'Pathé Tuschinski',
        'address': 'Reguliersbreestraat 26-34, 1017 CN Amsterdam',
    },
    {
        'tag': 'pathe-city',
        'name': 'Pathé City',
        'address': 'Kleine-Gartmanplantsoen 15-19, 1017 RP Amsterdam',
    },
    {
        'tag': 'pathe-amsterdam-noord',
        'name': 'Pathé Amsterdam-Noord',
        'address': 'Buikslotermeerplein 2003, 1025 XL Amsterdam',
    },
    {
        'tag': 'pathe-arena',
        'name': 'Pathé Arena',
        'address': 'Johan Cruijff Boulevard 600, 1101 DS Amsterdam',
    }
]


def get_json(url):
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/605.1.15 (KHTML, like Gecko) "
            "Version/26.0 Safari/605.1.15"
        ),
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "nl-NL,nl;q=0.9,en;q=0.8",
        "Referer": "https://www.pathe.nl/",
    }
    print(url)
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()

def get_cinema(cinema):
    url = f"https://www.pathe.nl/api/cinema/{cinema}"
    return get_json(url)

def get_shows(cinema):
    url = f"https://www.pathe.nl/api/cinema/{cinema}/shows"
    shows = get_json(url)
    return list(shows.get('shows').keys())

def get_show(show):
    url = f"https://www.pathe.nl/api/show/{show}?language=nl"
    return get_json(url)

def get_showtimes(show, cinema):
    url = f"https://www.pathe.nl/api/show/{show}/showtimes/{cinema}"
    return get_json(url)


def format_event(cinema, show, date_key, showtime):
    return {
        'date': date_key,
        'time': showtime['time'].split(' ')[1][:5],
        'title': show['title'],
        'venue': cinema['name'],
        'price': "",
        'site': showtime.get('refCmd'),
        'address': cinema['address'],
    }


def bot():
    all_events = []
    for cinema in cinemas:
        cinema_tag = cinema['tag']
        shows = get_shows(cinema_tag)

        for show_id in shows:
            show_data = get_show(show_id)
            showtimes_data = get_showtimes(show_id, cinema_tag)

            for date_key, showtime_list in showtimes_data.items():
                for st in showtime_list:
                    event = format_event(cinema, show_data, date_key, st)
                    all_events.append(event)
    return all_events

