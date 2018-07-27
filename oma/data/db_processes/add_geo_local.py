
import pandas as pd
import sqlite3


# db connection
conn = sqlite3.connect('oma.db')

# load file
data = pd.read_csv('geo_local.csv')
data.columns = ['cod_local', 'barrio', 'corregimiento', 'municipio',
                'departamento']

# filter departamentos
data.loc[data.departamento == 'MAGANGUE', 'DEPARTAMENTO'] = 'BOLIVAR'
dptos = ['ATLANTICO', 'BOLIVAR', 'CESAR', 'CORDOBA', 'LA GUAJIRA',
         'MAGDALENA', 'SUCRE']
data = data[data.departamento.isin(dptos)]
# add delegacion
mdel = pd.read_csv('geo_del.csv', encoding='iso-8859-1')
mdel.columns = ['municipio', 'departamento', 'delegacion']
data = pd.merge(data, mdel, on=['municipio', 'departamento'],
                left_index=False, right_index=False, sort=False,
                how='left')
del data['DEPARTAMENTO']
# insert into db
data.to_sql('geo_local', conn, if_exists='replace', index=False)
mdel.to_sql('delegaciones', conn, if_exists='replace', index=False)
conn.close()
