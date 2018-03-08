
import requests
import pandas as pd
import numpy as np
import time as ti
import sqlite3 

while True:
    response = requests.get("https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=TSLA&interval=1min&outputsize=full&apikey=HHONDLWYDYRV5NUE")

    print(response.status_code)

    js = response.json()
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
    up = data[data.shape[0]-1,:]
    print up
    print tuple(up)
    conn = sqlite3.connect('test1.db')
    c = conn.cursor()
    c.execute('INSERT INTO Stock_price VALUES(?, ?, ?, ?, ?, ?,?)',tuple(up))
    print "here"
    conn.commit()
    conn.close()
    ti.sleep(60)
   

    