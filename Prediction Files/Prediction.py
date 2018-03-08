#reference: https://pythonprogramming.net/forecasting-predicting-machine-learning-tutorial/ 
import sqlite3
import numpy as np 
import pandas as pd 
from sklearn import preprocessing, cross_validation
from sklearn import linear_model
import matplotlib.pyplot as plt


#read data from database
conn = sqlite3.connect('test2.db')
tesla = pd.read_sql_query('SELECT * FROM historical_price',conn)
#print tesla 

#create new varaibles 
#HL_PCT accounts for the rate of change between high price and low price 
#PCT_chage accounts fro the rate of change between open price and close price 
tesla['HL_PCT']= (tesla['High'] - tesla['Low']) / tesla['Close'] * 100.0
tesla['PCT_change'] = (tesla['Close'] - tesla['Open']) / tesla['Open'] * 100.0
#print tesla 


tesla = tesla[['Day','Close', 'HL_PCT', 'PCT_change', 'Volume']]
#print tesla
day=tesla.as_matrix(columns=['Day'])
#print day

#define independent variables & scale X
X = tesla.as_matrix(columns=['HL_PCT', 'PCT_change', 'Volume'])
X = preprocessing.scale(X)
#print X

#define dependent varaible Y
Y=tesla.as_matrix(columns=['Close'])
#print Y

#data split
X_train, X_test, Y_train, Y_test = cross_validation.train_test_split(X, Y, test_size=0.3)

#data training 
clf = linear_model.LinearRegression()
clf.fit(X_train, Y_train)

#evaluate prediction accuracy
confidence = clf.score(X_test, Y_test)
print confidence





