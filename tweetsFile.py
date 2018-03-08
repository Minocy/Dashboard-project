
# coding: utf-8

# In[1]:

import tweepy as ty
twitter_app_key = 'UZX4m9nbTGRLonkJ8uE59ntfg'
twitter_app_secret = '29gdg7BeW4NfwVS5kQUQ27LRUvYRS388eNT7LGEbp8XnGxkTlc'
twitter_key = '551548986-danfKYxtovQc1FIltEfvqiH5W3r9nmymjU0QQxAw'
twitter_secret = 'pcNCAmt5g6emZvhj3a5WdPzmTV9ZGse7M6lXDe7KagaDv'


# In[2]:

auth = ty.OAuthHandler(twitter_app_key, twitter_app_secret)
auth.set_access_token(twitter_key, twitter_secret )


# In[3]:

api = ty.API(auth)


# In[7]:




# In[ ]:


import dataset
from textblob import TextBlob
from sqlalchemy.exc import ProgrammingError
import json
import re

db = dataset.connect("sqlite:///tweets.db")

class StreamListener(ty.StreamListener):
    def clean_tweet(self, status):
        return ''.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())
      
    def on_status(self, status):
        if hasattr(status, 'retweeted_status'):
            return
        else:
            text = status.text
            description = status.user.description
            loc = status.user.location
            blob = TextBlob(text)
            sent = blob.sentiment
            print(text)
            
        
        table = db["tweets"]
        try:
            table.insert(dict(
                user_decription=description,
                user_location=loc,
                text=text,
                polarity = sent.polarity,
                subjctivity = sent.subjectivity,))
        except ProgrammingError as err:
            print(err)
    
    def on_error(self, status_code):
        if status_code == 420:
            return False

stream_listener = StreamListener()
stream = ty.Stream(auth=api.auth, listener=stream_listener)
stream.filter(languages=['en'], track=['tesla','model-s','self-driving'])


# In[13]:



