#!/usr/bin/env python3

from datetime import datetime
from time import sleep
import requests
import sys

import os
from dotenv import load_dotenv
load_dotenv()

CALENDARS = {
    "jazzAmsterdam" : {
        "user_id" : os.environ.get('INSTAGRAM_JAZZ_ID'),
        "user_token": os.environ.get('INSTAGRAM_JAZZ'),
        "caption": "#jazz #amsterdam\nhttps://jazzin.amsterdam"
    },
    "classicalAmsterdam" : {
        "user_id" : os.environ.get('INSTAGRAM_CLASSICAL_ID'),
        "user_token": os.environ.get('INSTAGRAM_CLASSICAL'),
        "caption" : "#classicalmusic #amsterdam\nhttps://jazzin.amsterdam/classical"
    },
    "theaterAmsterdam" : {
        "user_id" : os.environ.get('INSTAGRAM_THEATER_ID'),
        "user_token": os.environ.get('INSTAGRAM_THEATER'),
        "caption" : "#theater #amsterdam\nhttps://jazzin.amsterdam/theater"
    }
}

def make_screenshot(image_url):
    return requests.get(image_url).status_code

# def get_screenshot_link(calendar, format, date):
#     html_url = f"https://jina3.vercel.app/cal/{calendar}/today/{format}/html/{date}"
#     screenshot_data = {
#         "access_key" : os.environ.get('API_FLASH_KEY'),
#         "url": html_url,
#         # "response_type": "json",
#         "scale_factor": "2",
#         "quality": "100",
#         "element": "#container",
#         "wait_for": "#container",
#         "wait_until": "network_idle",
#         # "fresh": "true"
#     }
#     return requests.post('https://api.apiflash.com/v1/urltoimage', data=screenshot_data).json()


def make_container(user_id, user_token, image_url, format, caption = ""):
    endpoint = f"https://graph.instagram.com/v21.0/{user_id}/media"
    body = {
        "caption": caption,
        "image_url": image_url,
        "access_token": user_token,
    }
    if format == 'story':
        body["media_type"] = "STORIES"

    try:
        request = requests.post(endpoint, data=body)
        print(request.status_code)
        return request.json()["id"]
    except:
        print('error')
        print(requests.post(endpoint, data=body).json())

def make_post(user_id, user_token, container_id):
    endpoint = f"https://graph.instagram.com/v21.0/{user_id}/media_publish"
    body = {
        "creation_id": container_id,
        "access_token": user_token
    }
    SITE = requests.post(endpoint, data=body)
    return SITE

if __name__=="__main__":
    timestamp = datetime.today().isoformat()
    calendar, format = sys.argv[1:]
    image_url = f"https://jina3.vercel.app/cal/{calendar}/today/{format}/jpg/{timestamp}.jpeg"
    user_id = CALENDARS[calendar]["user_id"]
    user_token = CALENDARS[calendar]["user_token"]
    caption = CALENDARS[calendar]["caption"]

    print(user_id, user_token, caption)

    def print_end(start_time):
        print("{} seconds".format((datetime.today() - start_time).total_seconds()))

    print('\n')
    print("Start:")
    print(timestamp)

    print("\nRefresh token:")
    start_time = datetime.today()
    print(requests.get(f"https://graph.instagram.com/refresh_access_token?grant_type=ig_refresh_token&access_token={user_token}").status_code)
    print_end(start_time)

    print("\nMake screenshot:")
    start_time = datetime.today()
    print(make_screenshot(image_url))
    print_end(start_time)

    sleep(15)

    print("\nCheck screenshot:")
    start_time = datetime.today()
    print(make_screenshot(image_url))
    print_end(start_time)

    sleep(3)
    
    print("\nMake constainer:")
    start_time = datetime.today()
    container_id = make_container(user_id, user_token, image_url, format, caption)
    print_end(start_time)

    sleep(3)

    print("\nMake post:")
    start_time = datetime.today()
    print(make_post(user_id, user_token, container_id).status_code)
    print_end(start_time)

    print('\n')