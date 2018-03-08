import sqlite3
import pandas as pd 


#read data from database
conn = sqlite3.connect('test2.db')
tesla = pd.read_sql_query('SELECT * FROM historical_price',conn)
#convert it to csv file for later usage
Tesla = tesla.to_csv(path_or_buf='~/DS2/Projecta/Tesla.csv')
#print tesla 

