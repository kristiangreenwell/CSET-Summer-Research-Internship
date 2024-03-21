# This file gathers all the needed data from the specified Twitter accounts.
import tweepy
import csv

# Twitter API Access
client = tweepy.Client(
    bearer_token="AAAAAAAAAAAAAAAAAAAAAHEOoAEAAAAAo%2BfeC3U1htaX1Tnf6jR0kNxCRuA%3DSuT8QVRPGbNyD0qGZuGjB8MHEih3ZuzGbjhmr6OYlMSinlc357",
    consumer_key="kFQeL5oqK4WVJQLRj4EkXeDch",
    consumer_secret="La6Mwo4CJ5QFAipticyCfgcppICWnQvAXSzsOz8CKTH1arQnlo",
    access_token="1665776656814948352-x56a2SMpjqJ5IlDn2JEyNRrXU27Snv",
    access_token_secret="SM7ZSAYWXtwJQsyl1AZcnDWysYL5dcKL6XKIZFGBK5sNB",
)

'''Gets user ID - Andres Manuel'''
user = client.get_user(username="lopezobrador_")
user_ID = user.data.id

# Create file
csvfile = open('TwitterDataManuel.csv', 'w', newline='', encoding='utf-8')
c = csv.writer(csvfile)
c.writerow(['Tweet ID', 'Original Tweet', 'Preprocessed', 'Translated Tweet', 'Created At', 'Language'])

# Streaming a tweet
for tweet in tweepy.Paginator(client.get_users_tweets, user_ID, exclude=['retweets', 'replies'],
                              tweet_fields=['created_at'], max_results=100).flatten(limit=300):
    c.writerow([tweet.id, tweet.text, '', '', tweet.created_at, "es"])

csvfile.close()

'''Gets user ID - Sergio Ramos'''
user = client.get_user(username="SergioRamos")
user_ID = user.data.id

# Create file
csvfile = open('TwitterDataRamos.csv', 'w', newline='', encoding='utf-8')
c = csv.writer(csvfile)
c.writerow(['Tweet ID', 'Original Tweet', 'Preprocessed', 'Translated Tweet', 'Created At', 'Language'])

# Streaming a tweet
for tweet in tweepy.Paginator(client.get_users_tweets, user_ID, exclude=['retweets', 'replies'],
                              tweet_fields=['created_at'], max_results=100).flatten(limit=300):
    c.writerow([tweet.id, tweet.text, '', '', tweet.created_at, "es"])

csvfile.close()

'''Gets user ID - Bad Bunny'''
user = client.get_user(username="sanbenito")
user_ID = user.data.id

# Create file
csvfile = open('TwitterDataBunny.csv', 'w', newline='', encoding='utf-8')
c = csv.writer(csvfile)
c.writerow(['Tweet ID', 'Original Tweet', 'Preprocessed', 'Translated Tweet', 'Created At', 'Language'])

# Streaming a tweet
for tweet in tweepy.Paginator(client.get_users_tweets, user_ID, exclude=['retweets', 'replies'],
                              tweet_fields=['created_at'], max_results=100).flatten(limit=300):
    c.writerow([tweet.id, tweet.text, '', '', tweet.created_at, "es"])

csvfile.close()
