# Import necessary packages
import requests
from requests.auth import HTTPBasicAuth
import sys
from config import tokens  
import datetime
#import logging
import pymongo

sys.stdout.reconfigure(encoding='utf-8') # Useful for windows user

## AUTHENTIFICATION INFORMATION FOR YOUR REDDIT APP##
basic_auth = HTTPBasicAuth(
    username=tokens['client_id'], # the client id
    password=tokens['secret']  # the secret
)

GRANT_INFORMATION = dict(
    grant_type="password",
    username=tokens['username'], # REDDIT USERNAME
    password=tokens['password'] # REDDIT PASSWORD
)

headers = {
    'User-Agent': 'TestAppforDocker'
}

### URL TO REQUEST ACCESS TOKEN
POST_URL = "https://www.reddit.com/api/v1/access_token"


## REQUESTING A TEMPORARY ACCESS TOKEN ##
access_post_response = requests.post(
    url=POST_URL,
    headers=headers,
    data=GRANT_INFORMATION,
    auth=basic_auth
).json()

### ADDING TO HEADERS THE Authorization KEY (that we just got)

headers['Authorization'] = access_post_response['token_type'] + ' ' + \
                           access_post_response['access_token']

## Send a get request to download the latest (new) subreddits using the new headers.

topic = 'Berlin'
URL = f"https://oauth.reddit.com/r/{topic}/new"  # You could also select ".../hot" to fetch the most popular posts.

response = requests.get(
    url=URL,
    headers=headers  # this request would not work without the access token 
).json()

client = pymongo.MongoClient(host="mongodb", port=27017)
db = client.reddit

full_response = response['data']['children']

# Go through the full response and define a mongo_input dict
for post in full_response:

    _id = post['data']['id']
    subreddit_id = post['data']['subreddit_id']
    time = post['data']['created_utc']  # time in seconds since 1970
    time = datetime.datetime.fromtimestamp(time).strftime('%Y-%m-%d %H:%M:%S')
    subreddit = post['data']['subreddit']  # the above defined 'topic'
    title = post['data']['title']
    text = post['data']['selftext']  # the actual content
    author_fullname = post['data']['author_fullname']  # the actual content
    #logging.critical(post['data'].keys())

    if len(text) < 1:
        continue
    
    # shorten or lengthen mongo input as you deem fit: 
    mongo_input = {
        '_id': _id, 
        'title': title,
        'author_fullname': author_fullname,
        'sub_id': subreddit_id, 
        'date': time, 
        'text': text,
        }
    mongo_input = {'found_reddit': mongo_input}

    db.posts.insert_one(dict(mongo_input))
    # logging.critical(dict(mongo_input))
