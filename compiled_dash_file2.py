

import os
import pickle
import copy
import datetime as dt

import pandas as pd
from flask import Flask
from flask_cors import CORS
import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html


from dash.dependencies import Output, Event, Input
import plotly
import random
import plotly.graph_objs as go
import sqlite3
import pandas as pd
import time



app = dash.Dash('perfectdash')
app.css.append_css({'external_url': 'https://cdn.rawgit.com/plotly/dash-app-stylesheets/2d266c578d2a6e8850ebce48fdb52759b2aef506/stylesheet-oil-and-gas.css'})  # noqa: E501
server = app.server

# colorscale = cl.scales['9']['qual']['Paired'] 

# Read in real-time stock price 
import sqlite3 
conn = sqlite3.connect('test1.db')
c = conn.cursor()
f=pd.read_sql_query("SELECT * FROM Stock_price \
 where Day= (SELECT Day FROM Stock_price ORDER BY Day DESC LIMIT 1)", conn)

result=f.sort_values(by=['Time_value'])


x=result['Time_value']
y=result['Close']

# Read historical stock price 

conn2 = sqlite3.connect('test2.db')
h=pd.read_sql_query("SELECT * FROM historical_price", conn2)
h_x=h['Day']
h_y=h['Close']


# sentiment analysis 
import dataset
import nltk
import pandas as pd
import sqlite3
import string
import re
import plotly.plotly as py
import plotly.graph_objs as go

conn3 = sqlite3.connect("tweets.db")
c = conn3.cursor()
# c.execute("UPDATE tweets SET sentiment = 'positive' WHERE polarity > 0")
# c.execute("UPDATE tweets SET sentiment = 'negative' WHERE polarity < 0")
# c.execute("UPDATE tweets SET sentiment = 'neutral' WHERE polarity = 0")
# conn3.commit()

twtext = pd.read_sql_query('SELECT * FROM tweets', conn3)

tweets_texts = twtext['text'].tolist()

### number of positi
# pnn = twtext['sentiment'].value_counts().to_dict()

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

from nltk.util import ngrams
from collections import Counter
import numpy as np 

bigrams = ngrams(words,1)

s_data=Counter(bigrams)


words= Counter(s_data).most_common(15)

df = pd.DataFrame(data=words)
df.columns = ['words','count']

#df_new=df.set_index('words')

X=list(df['words'])
X_list = [list(x) for x in X]
labels  = [val for sublist in X_list for val in sublist]

Y=df['count']



# twtext = pd.read_sql_query('SELECT * FROM tweets', conn3)

app.layout = html.Div(
    [
        html.Div(
            [
                html.H1(
                    'Analytical Dashboard for Tesla Inc.',
                    className='eight columns',
                ),
                html.Img(
                     src="https://www.interiorsplash.com/hs-fs/hubfs/initech.png?width=1118&name=initech.png",
                    className='one columns',
                    style={
                        'height': '100',
                        'width': '225',
                        'float': 'right',
                        'position': 'relative',
                    },
                ),
            ],
            className='row'
        ),
        html.Div(
            [
                html.Div(
                    [
                        dcc.Graph(id='live-graph2', animate=True),
                        dcc.Interval(id='graph-update2',interval=1*3000),
                    ],
                    className='eight columns',
                    style={'margin-top': '20'}
                ),
                html.Div(
                    [
                        dcc.Graph(id='individual_graph', 
                            figure={
                    'data': [
                        {'x': h_x, 'y': h_y, 'type': 'line', 'name': 'historical stock'}
                     ,
                        ],
                    'layout': {
                        'title': 'Tesla Historical Stock Price (updated daily)'
                        }
                    })
                    ],
                    className='four columns',
                    style={'margin-top': '20'}
                ),
            ],
            className='row'
        ),
        html.Div(
            [
                html.Div(
                    [
                        dcc.Graph(id='count_graph',
                            figure={
                    'data': [
                        { 'x':[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15],'y': Y, 'type': 'bar', 'name': 'Words Frequency', 'text': labels,
                            }
                     ,
                        ],
                    'layout': {
                        'title': 'Text Analysis Words Frequency'
                        
                        }
                    })
                    ],
                    className='four columns',
                    style={'margin-top': '10'}
                ),
                html.Div(
                    [
                        dcc.Graph(id='live-graph', animate=False, 
                            figure={'layout': {
                        'title': 'Live Twitter Sentiment Score'}
                            }
                        ),
                        dcc.Interval(
                            id='sentiment_term',
                            interval=1*1000),
                    ],
                    className='four columns',
                    style={'margin-top': '10'}
                ),
                html.Div(
                    [
                        html.Img(
                         src="https://1drv.ms/u/s!AlYPmtP11H3cs08fKLvLSgFEHkBj",
                        className='one columns',
                        style={
                            'height': '100',
                            'width': '225',
                            'float': 'right',
                            'position': 'relative',
                         },
                    ),
                        # dcc.Graph(id='aggregate_graph')
                    ],
                    className='four columns',
                    style={'margin-top': '10'}
                ),
            ],
            className='row'
        ),
 
    ],
    className='ten columns offset-by-one'
)





@app.callback(Output('live-graph', 'figure'),
              [Input(component_id='sentiment_term', component_property='id')],
              events=[Event('sentiment_term', 'interval')])


def update_graph_scatter(sentiment_term):
    try:
        conn4 = sqlite3.connect('tweets.db')
        c = conn4.cursor()
        df = pd.read_sql("SELECT * FROM tweets", conn4)
        df.sort_values('id', inplace=True)
       


        df.dropna(inplace=True)

        X = df.id.values[-100:]
        Y = df.polarity.values[-100:]

        data = plotly.graph_objs.Scatter(
                x=X,
                y=Y,
                name='Scatter',
                mode= 'lines+markers'
                )

        return {'data': [data],'layout' : go.Layout(xaxis=dict(range=[min(X),max(X)]),
                                                    yaxis=dict(range=[min(Y),max(Y)]),
                                                    title='Term: {}'.format(sentiment_term))}

    except Exception as e:
        with open('errors.txt','a') as f:
            f.write(str(e))
            f.write('\n')


@app.callback(Output('live-graph2', 'figure'),
              events=[Event('graph-update2', 'interval')])
def update_graph_scatter():
    print "here"
    #X.append(X[-1]+1)
    X = []
    Y = []
    conn = sqlite3.connect('test1.db')
    c = conn.cursor()
    f=pd.read_sql_query("SELECT Time_value, Close FROM Stock_price where Day= (SELECT Day FROM Stock_price ORDER BY Day DESC LIMIT 1)", conn)
    r=f.sort_values(by=['Time_value'])
    X = list(r['Time_value'])
    Y = list(r['Close'])
    print type(X)
    data = plotly.graph_objs.Scatter(
            x=list(X),
            y=list(Y),
            name='Scatter',
            mode= 'lines+markers'
            )

    return {'data': [data]}




if __name__ == '__main__':
    app.run_server(debug=True)


