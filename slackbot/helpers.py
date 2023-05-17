from config import tokens
import sqlalchemy
import psycopg2
import time
#import logging

USERNAME_PG = tokens['username']
PASSWORD_PG = tokens['password']
HOST_PG = tokens['host']
PORT_PG = tokens['port']
DATABASE_NAME_PG = tokens['db_name']
WEBHOOK_URL = tokens['web_hook']

CONN_STRING_PG = f"postgresql://{USERNAME_PG}:{PASSWORD_PG}@{HOST_PG}:{PORT_PG}/{DATABASE_NAME_PG}"

def connect_to_db():
    """
    Establish a connection to the PostgreSQL database

    return: engine and connection to be closed after
    """
    time.sleep(120)
    
    eng = sqlalchemy.create_engine(CONN_STRING_PG, echo=True)
    pg = eng.connect()

    #logging.critical('Slackbot conected to postgres')

    return eng, pg

def get_reddits_from_db():
    """
    Extracts all reddits from Postgress db called reddits

    return: response
    """
    
    eng, pg = connect_to_db()

    query = sqlalchemy.text('SELECT * FROM reddits')
    response = pg.execute(query).mappings().all()

    # logging.critical(response[-1])

    #positive_reddits = [a['subreddit'] for a in response]

    eng.dispose()
    pg.close()
                
    return response

def get_formatted_data(reddits):

    # Extract the required fields for the message
    sentiment_score = reddits[-1]['sentiment']
    title = reddits[-1]['title']
    author_fullname = reddits[-1]['author_fullname']
    subreddit = reddits[-1]['subreddit']

    data = {
        'text': f'New reddit! Sentiment score: {sentiment_score}',
        'channel': '#angela_slackbot',
        'attachments': [
            {
                'title': f'{author_fullname}: {title}',
                'text': f'{subreddit}'
        }
    ]
    }  # Format the data so it can be posted to slack

    return data