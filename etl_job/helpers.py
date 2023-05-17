"""
Helper file with the helper functions needed during the ETL process.
"""

#import logging
import psycopg2
import pymongo 
import time
import sqlalchemy
from config import tokens
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# GLOBAL VARIABLES. 
# Keep in mind if we were using actual username and password
# (instead of the default ones to play), you would outsource them.

USERNAME_PG = tokens['username']
PASSWORD_PG = tokens['password']
HOST_PG = tokens['host']
PORT_PG = tokens['port']
DATABASE_NAME_PG = tokens['db_name']

CONN_STRING_PG = f"postgresql://{USERNAME_PG}:{PASSWORD_PG}@{HOST_PG}:{PORT_PG}/{DATABASE_NAME_PG}"

def get_collection_from_mongo():
    """
    Function to extract the wanted collection from the mongo db
    """
    client = pymongo.MongoClient('mongodb', port=27017)

    time.sleep(3)

    db = client.reddit
    coll = db.posts

    # logging.critical("\n---- Collection extracted ----\n")

    return coll

def regex_clean(text):
    """
    Clean the text from the reddits (links, blank spaces...)
    """
    # logging.critical(text)
    return text

def sentiment_analysis(text):
    """
    Exract a sentiment score for each text
    """
    analyser = SentimentIntensityAnalyzer()
    scores = analyser.polarity_scores(text)
    return scores['compound']

def connect_to_postgres():
    eng = sqlalchemy.create_engine(CONN_STRING_PG, echo=True)
    pg = eng.connect()
    time.sleep(3)

    # Create the table
    create_table_string = sqlalchemy.text("""CREATE TABLE IF NOT EXISTS reddits (
                                            id text primary key,
                                            title text,
                                            author_fullname text,
                                            sub_id text,
                                            date TEXT,
                                            subreddit TEXT,
                                            sentiment NUMERIC
                                            );
                                        """)

    pg.execute(create_table_string)
    pg.commit()

    return eng, pg