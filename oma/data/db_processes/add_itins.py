
import pandas as pd
import sqlite3


# load file
data = pd.read_csv('new_itins.csv')

# db connection
conn = sqlite3.connect('oma.db')

# process
query = """
    insert into info_itin (
    cod_unicom, ruta, num_itin,
    tipo1, tipo2, latitud,
    longitud, clientes, consumo,
    pcobro) values (
    {}, {}, {}, 
    '{}', '{}', {},
    {}, {}, {}, 
    {})
"""
for i in range(len(data)):
    row = data.values[i]
    conn.execute(query.format(
        row[1], row[2], row[3],
        row[8], row[9], row[15],
        row[16], row[4], row[5],
        row[6]
    ))
    conn.commit()
conn.close()
