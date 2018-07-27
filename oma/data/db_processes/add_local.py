
import numpy as np
import pandas as pd
import sqlite3
from tqdm import tqdm


# db connection
conn = sqlite3.connect('oma.db')

query = """
    update info_itin set
    cod_local = {}, tarifa = '{}' where 
    cod_unicom = {} and
    ruta = {} and
    num_itin = {}
"""

# load file
data = pd.read_csv('local_itins_tar.csv')
itins = np.unique(data.iloc[:, 5:8], axis=0)
# process
for i in tqdm(range(len(itins))):
    # filter data
    x = data[(data.UNICOM == itins[i, 0]) & (data.RUTA == itins[i, 1]) &
             (data.ITIN == itins[i, 2])]
    # choice hight clientes
    x = x.loc[x.SUMINISTROS.idxmax()]
    # insert db
    conn.execute(query.format(x.CODLOCAL, x.TARIFA, x.UNICOM, x.RUTA, x.ITIN))
    conn.commit()
conn.close()


"""
Index(['DEPARTAMENTO', 'MUNICIPIO', 'CORREGIMIENTO', 'BARRIO', 'CODLOCAL',
       'UNICOM', 'RUTA', 'ITIN', 'TARIFA', 'SUMINISTROS'],
      dtype='object')
"""