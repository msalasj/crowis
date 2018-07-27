
from datetime import datetime

import glob
import pandas as pd
import sqlite3


# db connection
conn = sqlite3.connect('../oma.db')

# process
query1 = """
    insert into fechas_itin (
    cod_unicom, ruta, num_itin,
    periodo, f_plan, clientes,
    consumo, pcobro) values (
    {}, {}, {}, {},
    {}, {}, {}, {})
"""
query2 = """
    insert into fechas_itin (
    cod_unicom, ruta, num_itin,
    periodo, f_plan) values (
    {}, {}, {}, {}, {})
"""
files = glob.glob('v3/*.csv')
for i in range(len(files)):
    data = pd.read_csv(files[i])
    for j in range(len(data)):
        # 201712
        row = data.values[j]
        periodo = int(datetime.strptime(row[7], "%d/%m/%Y").strftime('%Y%m'))
        f_plan = int(datetime.strptime(row[7], "%d/%m/%Y").timestamp())
        conn.execute(query1.format(
            row[1], row[2], row[3], periodo,
            f_plan, row[4], row[5], row[6]))
        conn.commit()
        # 2018
        for k in range(19, 31):
            periodo = int(datetime.strptime(row[k], "%d/%m/%Y").strftime('%Y%m'))
            f_plan = int(datetime.strptime(row[k], "%d/%m/%Y").timestamp())
            conn.execute(query2.format(
                row[1], row[2], row[3], periodo, f_plan))
            conn.commit()
    print(files[i])
conn.close()

"""
    ['COD', 'UNICOM', 'RUTA', 'ITIN', 'CLIENTES', 'CONSUMO', 'IMPORTE',
    'F_INI', 'TIPO1', 'TIPO2', 'DELEGACION', 'DEPARTAMENTO', 'MUNICIPIO',
    'CORREGIMIENTO', 'BARRIO', 'LAT', 'LON', 'DIA', 'NEW_DAY', '2018-01',
    '2018-02', '2018-03', '2018-04', '2018-05', '2018-06', '2018-07',
    '2018-08', '2018-09', '2018-10', '2018-11', '2018-12'],
"""
