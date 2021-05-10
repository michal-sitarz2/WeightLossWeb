import requests
import tweepy
import threading

consumer_key = 'Lx4vGoV6UaaBaXsfGAkDIDoDn'
consumer_secret_key = 'KgQecSB0X7wpiG0abEZF79zmIkcKzZRy2naAXjxNbDeGdmHnIO'

access_token = '1382365409157001223-GovkCrgtbNf7MIj1y2hUw0q12x8whv'
access_token_secret = 'Pm4cBlYtqjzbhaPu2OHItyiH9xfLs9UTcnOdUuEwy6efi'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret_key)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, wait_on_rate_limit=True)

listening_thread = threading.Thread()

class MyStreamListener(tweepy.StreamListener):

    def on_status(self, status):
        # This should probably return the link so that it can be displayed, right now it just prints the tweet link to the console.
        print('https://twitter.com/' + status.user.screen_name + '/status/' + str(status.id))


def stream_tweets():
    myStreamListener = MyStreamListener()
    myStream = tweepy.Stream(auth=api.auth, listener=myStreamListener, thread=listening_thread)
    # Trump is just used here to test the streaming as it's a very high traffic term
    myStream.filter(track=['Diet','Trump','Nutrition'], is_async=True) # track= for keywords, follow= for the specific users.


# Function to extract tweets
def fetch_tweets(username):
    
    tweets = api.user_timeline(screen_name=username, exclude_replies=True)
  
    # Empty Array
    tweet_list=[] 
  
    # create array of tweet information: username, 
    # tweet id, date/time, text
    tweets_for_csv = [tweet.text for tweet in tweets] # CSV file created 
    for j in tweets_for_csv:
  
        # Appending tweets to the empty array tweet_list
        tweet_list.append(j) 
  
    # Formatting the tweets so that we can embed them
    tweet_ids = []
    for status in tweets:
        tweet_ids.append('https://twitter.com/' + status.user.screen_name + '/status/' + str(status.id))

    return tweet_ids
