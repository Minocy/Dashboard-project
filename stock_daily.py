import datetime as dt
import pandas as pd
import pandas_datareader.data as web
import numpy as np 

start = dt.datetime(2013, 1, 1)
end = dt.date.today() 

df = web.DataReader('TSLA', "google", start, end)
df.reset_index(inplace=True) # reset index (datetime) to column 
df['Date'] = df['Date'].astype(str) # convert timestamp to object 
data=np.array(df)

# use function to store data to sqlite

import sqlite3 

conn = sqlite3.connect('test2.db')
c = conn.cursor()
c.execute('CREATE TABLE historical_price(Day DATETIME, Open INTEGER, High INTEGER, Low INTEGER, \
	Close INTEGER, Volume INTEGER)')

for row in data:
    c.execute('INSERT INTO historical_price VALUES(?, ?, ?, ?, ?, ?)',tuple(row))

# c.execute('SELECT * from historical_price')
# print c.fetchall()

#f=pd.read_sql_query("select * from historical_price", conn)
#f.head() 

conn.commit()
conn.close()

