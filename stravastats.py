# Det här kan ju bli intressant när Strava väl gör ett användbart API....

import os
import requests
from dotenv import load_dotenv


# Load variables
load_dotenv() # local tests
REQUEST_BASE = 'https://www.strava.com/api/v3'

def get_headers():
    payload = {
        'client_id': os.getenv('CLIENT_ID'),
        'client_secret': os.getenv('CLIENT_SECRET'),
        'refresh_token': os.getenv('STRAVA_REFRESH_TOKEN'),
        'grant_type': 'refresh_token',
        'f': 'json'
    }
    res = requests.post("https://www.strava.com/oauth/token", data=payload, verify=False)
    access_token = res.json()['access_token']
    headers =  {'Authorization': f'Authorization: Bearer {access_token}'}
    return headers

def get_athlete_activities():
    headers = get_headers()
    res = requests.get(REQUEST_BASE + '/athlete/activities', headers=headers).json()
    return res

def get_club_activities(club_nr): # vafaaaaan... finns varken id på aktiviteten eller datum
    headers = get_headers()
    res = requests.get(REQUEST_BASE + f'/clubs/{club_nr}/activities', headers=headers).json()
    return res