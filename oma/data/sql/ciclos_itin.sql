select
COD_UNICOM,
RUTA,
NUM_ITIN,
CICLO,
F_LTEOR,
F_LREAL,
F_FACT
from ciclos_itin
where F_LTEOR 
BETWEEN TO_DATE('01/12/2017', 'DD/MM/YYYY')
AND TO_DATE('31/12/2018', 'DD/MM/YYYY)