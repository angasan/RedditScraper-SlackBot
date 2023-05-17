"""
ETL job broken down. 
Consists of:
- Extraction of the reddits from Mongo db
- Transformation of the reddits
- Sentiment Analysis
- Load reddits to Postgres db
"""

#import logging
import sqlalchemy
from helpers import (
    regex_clean, 
    sentiment_analysis,
    get_collection_from_mongo,
    connect_to_postgres
)

def extract(limit=5):
    """
    Extract the reddits from the given collection in mongodb
    """
    coll = get_collection_from_mongo()
    limit = coll.count_documents({}) 

    # keep in mind the line above is only bc the amount of reddits is limited!!!
    extracted_reddits = list(coll.find(limit=limit))
    #logging.critical(f"\n---- {limit} reddits extracted ----\n")

    return extracted_reddits

def transform(extracted_reddits):
    transformed_reddits = []

    for item in extracted_reddits:
        # Extract the text
        post = item['found_reddit']
        text = post['text']

        # Text processing
        text = regex_clean(text)
        sentiment = sentiment_analysis(text)

        # Adding the sentiment field to the post
        post['sentiment'] = sentiment

        # Append the transformed reddit to the list to be returned
        transformed_reddits.append(post)
        #logging.critical("\n---- reddit transformed ----\n")

    return transformed_reddits

def load(transformed_reddits):
    eng, pg = connect_to_postgres()

    for post in transformed_reddits:

        insert_query = sqlalchemy.text(
            """
            INSERT INTO reddits (
                id, 
                title,
                author_fullname,
                sub_id, 
                date, 
                subreddit, 
                sentiment
                )
            VALUES (
                :id, :title, :author_fullname, :sub_id, :date, :subreddit, :sentiment
                )
            ON CONFLICT (id) DO UPDATE 
                SET date = excluded.date,
                    title = excluded.title,
                    author_fullname = excluded.author_fullname,
                    sub_id = excluded.sub_id,
                    subreddit = excluded.subreddit,
                    sentiment = excluded.sentiment
            """
            )
        
        pg.execute(insert_query, {'id': post['_id'], 
                                  'title': post['title'],
                                  'author_fullname': post['author_fullname'],
                                  'sub_id': post['sub_id'], 
                                  'date': post['date'], 
                                  'subreddit':post['text'], 
                                  'sentiment': post['sentiment']}
                                  )
        
        pg.commit()

        #logging.critical("\n---- reddit loaded ----\n")

    return eng, pg