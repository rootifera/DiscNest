import os
import requests
import time
from dotenv import load_dotenv

load_dotenv()

TWITCH_CLIENT_ID = os.getenv("TWITCH_CLIENT_ID")
TWITCH_CLIENT_SECRET = os.getenv("TWITCH_CLIENT_SECRET")

def get_twitch_token():
    url = "https://id.twitch.tv/oauth2/token"
    params = {
        "client_id": TWITCH_CLIENT_ID,
        "client_secret": TWITCH_CLIENT_SECRET,
        "grant_type": "client_credentials"
    }
    resp = requests.post(url, params=params)
    resp.raise_for_status()
    return resp.json()["access_token"]

def igdb_search_game(game_name, token):
    headers = {
        "Client-ID": TWITCH_CLIENT_ID,
        "Authorization": f"Bearer {token}",
    }
    data = f'search "{game_name}"; fields name, first_release_date, genres.name, platforms.name, involved_companies.company.name, cover.url, summary;'
    resp = requests.post("https://api.igdb.com/v4/games", headers=headers, data=data)
    resp.raise_for_status()
    return resp.json()

def format_year(timestamp):
    try:
        return time.strftime('%Y', time.gmtime(timestamp))
    except Exception:
        return "-"

def igdb_get_game_details(game_id, token):
    headers = {
        "Client-ID": TWITCH_CLIENT_ID,
        "Authorization": f"Bearer {token}",
    }
    fields = (
        "name, summary, first_release_date, genres.name, "
        "themes.name, game_modes.name, player_perspectives.name, "
        "involved_companies.company.name, involved_companies.developer, involved_companies.publisher, "
        "platforms.name, cover.url, screenshots.url"
    )
    data = f'fields {fields}; where id = {game_id};'
    resp = requests.post("https://api.igdb.com/v4/games", headers=headers, data=data)
    print(f"IGDB REQUEST DATA: {data}")  # debug
    print(f"IGDB RESPONSE: {resp.status_code} {resp.text}")  # debug
    resp.raise_for_status()
    results = resp.json()
    if results:
        return results[0]
    else:
        return None

