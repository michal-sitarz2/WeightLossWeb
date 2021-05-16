import requests
import tweepy
import threading
import django.dispatch

consumer_key = 'Lx4vGoV6UaaBaXsfGAkDIDoDn'
consumer_secret_key = 'KgQecSB0X7wpiG0abEZF79zmIkcKzZRy2naAXjxNbDeGdmHnIO'

access_token = '1382365409157001223-GovkCrgtbNf7MIj1y2hUw0q12x8whv'
access_token_secret = 'Pm4cBlYtqjzbhaPu2OHItyiH9xfLs9UTcnOdUuEwy6efi'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret_key)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, wait_on_rate_limit=True)

listening_thread = threading.Thread()
'''
We define a signal type to be raised when the stream receives a new tweet. This
lets us be notified in other parts of the application. For more on signals see
https://docs.djangoproject.com/en/3.2/topics/signals
'''
tweet_received = django.dispatch.Signal()


class MyStreamListener(tweepy.StreamListener):
    def on_status(self, status):
        self.send_signal('https://twitter.com/' + status.user.screen_name + '/status/' + str(status.id))
        
    def send_signal(self, url):
        tweet_received.send(sender=self.__class__, url=url)


    def on_error(self, status_code):
        if status_code == 420:
            return False
        return True


def stream_tweets(request, tweets):

    myStreamListener = MyStreamListener()
    myStream = tweepy.Stream(auth=api.auth, listener=myStreamListener, thread=listening_thread)

    # I think we should be tracking these from accounts not keywords. Twitter content is mostly irrelevant to us with keywords
    myStream.filter(track=['Diet','Nutrition'], is_async=True) # track= for keywords, follow= for the specific users.



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

    return tweet_ids[:10] # Limit the tweet count
