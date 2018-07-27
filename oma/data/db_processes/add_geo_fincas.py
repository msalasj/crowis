
import pandas as pd
import sqlite3


# db connection
conn = sqlite3.connect('oma.db')

# load file
data = pd.read_csv('geo_nif.csv')
data.columns = ['nif', 'latitud', 'longitud']
data.to_sql('geo_fincas', conn, if_exists='replace', index=False)

conn.close()
