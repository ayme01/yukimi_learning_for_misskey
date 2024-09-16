from misskey import Misskey
from misskey.exceptions import MisskeyAPIException
import json
import requests
from logging import getLogger
logger = getLogger(__name__)

with open('../config.json', 'r') as json_file:
    config = json.load(json_file)

# Misskey.py API
misskey = Misskey(config['token']['server'], i=config['token']['i'])
i_id = misskey.i()["id"]
followers_data_url = f"https://{config['token']['server']}/api/users/followers"
follow_url = f"https://{config['token']['server']}/api/following/create"

def get_followers():
    followers_len = misskey.i()["followersCount"]
    followers = get_limit_followers()
    followers_count = 0
    followers_ids = []
    until_id = followers[-1]["id"]
    while len(followers) <= followers_len:
        followers += get_limit_followers(until_id=until_id)
        if followers_count == len(followers):
            break
        else:
            until_id = followers[-1]["id"]
            followers_count = len(followers)
    for f in followers:
        if f["follower"]["isFollowing"] == False and f["follower"]["name"] != None:
            followers_ids.append(f)
    return followers_ids

def get_limit_followers(until_id=None):
    limit = 100
    if until_id:
        get_tl_json_data = {
            "i": config["token"]["i"],
            "limit": limit,
            "untilId": until_id,
            "userId": i_id
        }
    else:
        get_tl_json_data = {
            "i": config["token"]["i"],
            "limit": limit,
            "userId": i_id
        }
    
    response = requests.post(
        followers_data_url,
        json.dumps(get_tl_json_data),
        headers={'Content-Type': 'application/json'})
    return response.json()

def follow_back():
    followers = get_followers()
    for f in followers:
        try:
            misskey.following_create(f["followerId"])
        except MisskeyAPIException as e:
            if e.code == "RATE_LIMIT_EXCEEDED":
                print("RATE_LIMIT_EXCEEDED")
                break
