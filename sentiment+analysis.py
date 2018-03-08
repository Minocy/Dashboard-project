
# coding: utf-8

# In[1]:

import dataset
import nltk
import pandas as pd
import sqlite3
import string
import re
import plotly.plotly as py
import plotly.graph_objs as go


# In[2]:

conn = sqlite3.connect("tweets.db")
c = conn.cursor()




# In[3]:

twtext = pd.read_sql_query('SELECT * FROM tweets', conn)

tweets_texts = twtext['text'].tolist()




# In[5]:

twtext.count()


# In[77]:

### number of positi
pnn = twtext['sentiment'].value_counts().to_dict()
print (pnn)


# In[78]:




# In[ ]:




# In[15]:

import string
from nltk.corpus import stopwords 
from nltk.tokenize import TweetTokenizer
# removing puncatuation and stopwords
def text_process(mess):
    mess = re.sub(r'\$\w*','',mess)
    mess = re.sub(r'https?:\/\/.*\/\w*','',mess)
    #mess = re.sub(r'['+string.punctuation+']+', ' ',mess)
    nopunc = [char for char in mess if char not in string.punctuation]
    nopunc = ''.join(nopunc)
    twtok = TweetTokenizer(strip_handles=True, reduce_len=True)
    tokens = twtok.tokenize(nopunc)
    tokens = [word for word in tokens if word.lower() not in stopwords.words('english')]
    return tokens
words = []
for tw in tweets_texts:
    words += text_process(tw)


# In[45]:


print(words)


# In[1]:

#https://www.analyticsvidhya.com/blog/2017/01/sentiment-analysis-of-twitter-posts-on-chennai-floods-using-python/


# In[ ]:




# In[46]:

from nltk.util import ngrams
from collections import Counter
bigrams = ngrams(words,2)
#print(Counter(bigrams))


# In[ ]:



