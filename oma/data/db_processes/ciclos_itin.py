
# from data.db_processes.db_connectors import OpenConnector

from datetime import datetime
import pandas as pd
import sqlite3


# Open Connection
conn = sqlite3.connect('../oma.db')
data = pd.read_csv('files/ciclos_itin.csv')
data = data[['COD_UNICOM', 'RUTA', 'NUM_ITIN', 'F_LTEOR', 'F_LREAL', 'F_FACT']]
query = """
    update fechas_itin set
    f_plan = {}, f_real = {}, f_fact = {}
    where cod_unicom = {} 
    and ruta = {} 
    and num_itin = {}
    and periodo = {}
"""
for i in range(len(data)):
    row = data.iloc[i]
    periodo = int(datetime.strptime(row.F_LTEOR, "%Y-%m-%d").strftime('%Y%m'))
    fplan = int(datetime.strptime(row.F_LTEOR, "%Y-%m-%d").timestamp())
    freal = int(datetime.strptime(row.F_LREAL, "%Y-%m-%d 00:00:00").timestamp())
    ffact = int(datetime.strptime(row.F_FACT, "%Y-%m-%d 00:00:00").timestamp())
    sql = query.format(fplan, freal, ffact, row.COD_UNICOM, row.RUTA, row.NUM_ITIN, periodo)
    conn.execute(sql)
    conn.commit()
conn.close()
print('Process Finished')
