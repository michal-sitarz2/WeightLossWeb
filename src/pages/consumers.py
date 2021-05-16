import json
from random import randint
from time import sleep
from .twitter import *

from channels.generic.websocket import WebsocketConsumer
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from micawber.contrib.mcdjango import oembed_html

# Suppress bs4 from complaining about html
import warnings
warnings.filterwarnings("ignore", category=UserWarning, module='bs4')

# Initialise the tweet stack
tweets = fetch_tweets('FitBottomedGirl')
for i in range(len(tweets)):
    tweets[i] = oembed_html(tweets[i])

class WSConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = 'tweet'
        self.room_group_name = self.room_name+"_room"
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept()
        stream_tweets()
        #self.send(json.dumps({'message': tweet_callback()}))
        #sleep(1)

    def update_tweets(self, data):
        self.send(json.dumps({'message': data['tweets']}))


def tweet_callback(sender, url, **kwargs):
    channel_layer = get_channel_layer()
    tweets.insert(0, oembed_html(url))
    tweets.pop()
    
    #print(oembed_html(url))
    async_to_sync(channel_layer.group_send)(
        'tweet_room',
        {
            'type': 'update_tweets',
            'tweets': tweets,
        }
    )

tweet_received.connect(tweet_callback)
