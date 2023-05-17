# Reddit Scraper and Slack Bot

This project extracts reddits from the Reddit API, processes them to get a sentiment score and posts them on your slack together with the sentiment score! 

To be more exact, I'm:  
1. Scraping reddits about Berlin from the Reddit API
2. Uploading them to a Mongodb database
3. Processing them using a Sentiment analysis open source code
4. Uploading the processed reddits to a PostgreeSQL database
5. Posting them on Slack using a slackbot
