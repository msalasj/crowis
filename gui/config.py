
# db parameters:
ip = '10.240.142.101'
port = '2050'
SID = 'PRODVG'
user = 'pase01'
password = 'pase02'
# en pase
user2 = 'modf_abar'
pass2 = 'm201712a'

# email
# emailto = ['jonate.crowis@gmail.com']
emailto = [
    'zpaulo1@ises.com.co',
    'manuel.campo@bureauveritasnla.com',
    'hramos@ises.com.co',
    'nguerraa@electricaribe.co',
    'jonate.crowis@gmail.com'
]
html_message = """
    <div>
    <h2 style="font-family: 'monospace', monospace;">GUI: Generaci&oacute;n de Universos de Interventor&iacute;a</h2>
    <div>
    <p style="font-family: 'monospace', monospace; margin: 30; padding: 0; font-size: 12px; line-height: 24px">{}</p>
    </div>
    <div>
    <img src="D:\Applications\crowis\lecturas\gui\im\crowis.png" width="120" height="40"/>
    </div>
    <div>
    <p style="font-family: 'monospace', monospace; margin: 0; padding: 0; font-size: 10px; line-height: 12px"><b>Jos&eacute; O&ntilde;ate L&oacute;pez</b></p>
    <p style="font-family: 'monospace', monospace; margin: 0; padding: 0; font-size: 10px; line-height: 12px"><a href="mailto:jonate.crowis@gmail.com">jonate.crowis@gmail.com</a></p>
    </div>
    </div>
"""
email_subject = 'GUI Notification'
email_attachments = []
report_message = """
    Adjunto se encuentran los universos a gestionar para cada una de las delegaciones.
"""

# on error
error_emailto = 'jonate.crowis@gmail.com'
error_message = 'Error detectado ejecutando la aplicación.'

# universe generation
wd = 10  # work days
ud = 60  # max number of users x day

# asociado comercial
asociado_comercial = {
    'DELTEC': ['Atlantico Norte', 'Atlantico Sur', 'Bolivar Norte', 'Bolivar Sur'],
    'LECTA': ['Cesar', 'Guajira', 'Magdalena'],
    'SERVICER': ['Cordoba Norte', 'Cordoba Sur', 'Sucre'],
}

# column order
column_order = ['NIS',	'NIC',	'NIF',	'NUM_APA',	'COD_UNICOM',	'RUTA',	'NUM_ITIN',	'CODIGO',	'DESCRIPCION',
                'ORIGEN',	'TARIFA',	'LATITUD',	'LONGITUD',	'DEPARTAMENTO',	'MUNICIPIO',	'CORREGIMIENTO',
                'BARRIO',	'VIA',	'NOM_CALLE',	'DUPLICADOR',	'NUM_PUERTA',	'MARCA_MEDIDOR',
                'ULTIMA_LECTURA',	'PENULTIMA_LECTURA',	'ANOMALIA_REPORTADA',	'FECHA_REPORTE_ANOMALIA',
                'ASOCIADO_COMERCIAL',	'DELEGACION',	'PROCESO',	'TIPOEQUIPO',	'NOM_CLIENTE']

# reclamos to filter
cod_reclamos = ['ZO011', 'ZO013', 'ZO015', 'ZO019', 'ZO029', 'ZO031', 'ZO051']
