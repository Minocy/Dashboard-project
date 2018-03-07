import requests
import pandas as pd
import numpy as np

# request the latest position of ISS
response = requests.get("https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=TSLA&interval=1min&outputsize=full&apikey=HHONDLWYDYRV5NUE")

# show the status of this request
print(response.status_code)

js = response.json()

# pretty print the data
# import pprint
# pp = pprint.PrettyPrinter()
# pp.pprint(js)  

# get time and value from json file 
value=js.get("Time Series (1min)") 
df1=pd.DataFrame(value).transpose()
df1=np.array(df1)

# get timestamp 
time=value.keys() 
df2=pd.DataFrame(time)
df2.columns=['Timestamp']
df2[['Date','Time']] = df2.pop('Timestamp').str.split(expand=True)

# split date and time 
df2=df2.sort_values(['Date','Time'], ascending=[True,True]) 
df2=np.array(df2)

# combine datetime and data frameworks 
data=np.concatenate((df2,df1),axis=1) 

# read data into sql database 
import sqlite3 

conn = sqlite3.connect('test1.db')
c = conn.cursor()
#c.execute('CREATE TABLE Stock_price(Day DATETIME, Time_value DATETIME, Open INTEGER, High INTEGER, Low INTEGER, \
#	Close INTEGER, Volume INTEGER)')

for row in data:
    c.execute('INSERT INTO Stock_price VALUES(?, ?, ?, ?, ?, ?,?)',tuple(row))

#c.execute('SELECT * from Stock_price')

# c.execute('SELECT name FROM sqlite_master WHERE type=\'table\'')
# print c.fetchall()
# c.execute('SELECT sql FROM sqlite_master WHERE type=\'table\' AND name=\'Stock_price\'')
#print c.fetchall()

# f=pd.read_sql_query("select * from Stock_price", conn)
# f.tail() 

f=pd.read_sql_query("SELECT * FROM Stock_price \
 where Day= (SELECT Day FROM Stock_price ORDER BY Day DESC LIMIT 1)", conn)

conn.commit()
conn.close()

print f

