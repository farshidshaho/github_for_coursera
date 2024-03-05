import os
import tweepy as tw
import pandas as pd
from tqdm import tqdm, notebook

from kaggle_secrets import UserSecretsClient
user_secrets = UserSecretsClient()

consumer_api_key = user_secrets.get_secret("CONSUMER_API_KEY")
consumer_api_secret = user_secrets.get_secret("CONSUMER_API_SECRET")


auth = tw.OAuthHandler(consumer_api_key, consumer_api_secret)
api = tw.API(auth, wait_on_rate_limit=True)


search_words = "#datascience -filter:retweets"
date_since = "2021-01-01"
# # Collect tweets
tweets = tw.Cursor(api.search_tweets,
              q=search_words,
              lang="en",
              since=date_since).items(500)


tweets_copy = []
for tweet in tqdm(tweets):
     tweets_copy.append(tweet)



print(f"new tweets retrieved: {len(tweets_copy)}")


tweets_df = pd.DataFrame()
for tweet in tqdm(tweets_copy):
    hashtags = []
    try:
        for hashtag in tweet.entities["hashtags"]:
            hashtags.append(hashtag["text"])
        text = api.get_status(id=tweet.id, tweet_mode='extended').full_text
    except:
        pass
    tweets_df = tweets_df.append(pd.DataFrame({'user_name': tweet.user.name, 
                                               'user_location': tweet.user.location,
                                               'user_description': tweet.user.description,
                                               'user_created': tweet.user.created_at,
                                               'user_followers': tweet.user.followers_count,
                                               'user_friends': tweet.user.friends_count,
                                               'user_favourites': tweet.user.favourites_count,
                                               'user_verified': tweet.user.verified,
                                               'date': tweet.created_at,
                                               'text': text, 
                                               'hashtags': [hashtags if hashtags else None],
                                               'source': tweet.source,
                                               'is_retweet': tweet.retweeted}, index=[0]))
    
tweets_df.head()





