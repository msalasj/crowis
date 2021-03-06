select   
anomaf.NIS,
anomaf.NIC,
anomaf.FECHA_REPORTE_ANOMALIA,
anomaf.CODIGO,
anomaf.ANOMALIA_REPORTADA, 
s.NIF,
mt.DESC_TIPO as TARIFA,
s.COD_UNICOM,
fpl.RUTA,
fpl.NUM_ITIN,
ap.NUM_APA,
cod.DESC_COD as MARCA_MEDIDOR,
co.LECT as ULTIMA_LECTURA,
(nom_cli || ' ' || Ape1_cli || ' ' || Ape2_cli) as NOM_CLIENTE,
nom_local as BARRIO,
nom_munic as CORREGIMIENTO,
nom_depto as MUNICIPIO,
nom_prov as DEPARTAMENTO,
rtrim(t.DESC_TIPO) as VIA,
rtrim(nom_calle) as NOM_CALLE,
f.duplicador,
f.num_puerta
from
sumcon s, clientes cl, fincas f, callejero c, localidades l, deptos d, 
municipios m, tipos t, provincias p, fincas_per_lect fpl, apmedida_ap ap,
codigos cod, apmedida_co co,
(select cod_tar, desc_tipo
from mtarifas, tipos 
where tip_util = tipo) mt,
(select 
NIS_RAD as NIS,
NIC,
F_UCE as FECHA_REPORTE_ANOMALIA,
CO_AN as CODIGO,
DESC_COD as ANOMALIA_REPORTADA
from 
trabpend_af taf, an_trabpend_af ataf, codigos cods
where 
EST_AF = 'SA400'
and ataf.num_af = taf.num_af
and cods.cod = CO_AN
and F_UCE > trunc(sysdate)-8) anomaf
where 
s.NIS_RAD = anomaf.NIS 
and s.tip_serv = 'SV100' 
and s.nif = f.nif 
and f.cod_calle = c.cod_calle 
and c.cod_local = l.cod_local 
and c.cod_depto = d.cod_depto 
and c.cod_munic = m.cod_munic 
and c.cod_prov = p.cod_prov 
and c.tip_via = t.tipo
and cl.cod_cli = s.cod_cli
and s.COD_TAR = mt.COD_TAR
and s.nif = fpl.nif
and s.NIS_RAD = ap.NIS_RAD
and ap.CO_MARCA = cod.COD
and ap.NUM_APA = co.NUM_APA
and co.F_LECT > TRUNC(SYSDATE) - 30