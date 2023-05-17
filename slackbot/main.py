# pip install pyjokes
import requests
from config import tokens
from helpers import (
    get_reddits_from_db,
    get_formatted_data,
    WEBHOOK_URL
    )

if __name__ == '__main__':

    # Get reddits from Postgres db
    reddits = get_reddits_from_db()  

    # Get the formatted data for posting
    data = get_formatted_data(reddits)

    # Post data to slack
    requests.post(url=WEBHOOK_URL, json = data) 
