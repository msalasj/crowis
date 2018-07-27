
import cx_Oracle
import glob
import logging
import numpy as np
import os
import pandas as pd
import sys
# import win32com.client as win32


def db_connector(cfg):
    dsn_str = cx_Oracle.makedsn(cfg.ip, cfg.port, cfg.SID)
    conn = cx_Oracle.connect(
        user=cfg.user,
        password=cfg.password,
        dsn=dsn_str,
        encoding='iso-8859-1'
    )
    logging.info('Conectado correctamente a Open: {},{},{}'.format(
        cfg.ip, cfg.port, cfg.SID
    ))
    return conn


def get_data(cfg):
    # data files validation
    data_files = glob.glob('db/data/*.csv')
    data = pd.DataFrame()
    if len(data_files) > 0:
        for data_fname in data_files:
            datai = pd.read_csv(data_fname)
            if 'reclamos' in data_fname:
                datai = datai.loc[datai['CODIGO'].isin(cfg.cod_reclamos)]
            data = pd.concat(
                [data, datai],
                ignore_index='True'
            )
            logging.info('File ' + data_fname + ' loaded')
    else:
        # db connection
        conn = db_connector(cfg)
        # extraer datos
        sql_files = glob.glob('db/sql/*.sql')
        for sql_fname in sql_files:
            sql = open(sql_fname).read()
            datai = pd.read_sql(sql, conn)
            if 'reclamos' in sql_fname:
                datai = datai.loc[datai['CODIGO'].isin(cfg.cod_reclamos)]
            data = pd.concat(
                [data, datai],
                ignore_index='True'
            )
            logging.info('Query ' + sql_fname + ' executed')
    return data


def data_wrangling(data, cfg):
    # TODO: filter data based on history db
    # unique nis
    _, pnis = np.unique(data.NIS, return_index=True)
    data = data.iloc[pnis, :]
    logging.info('unique NIS filter')
    # Filtrar Telemedidos: MARCA_MEDIDOR NSI
    data = data[~data['MARCA_MEDIDOR'].str.contains("NSI")]
    logging.info('MARCA_MEDIDOR NSI filtered')
    # origen: ANOMALIAS, ANOM FACTURACION, RECLAMOS
    data = data.assign(ORIGEN='')
    data.loc[data['CODIGO'].str.contains("ZO"), 'ORIGEN'] = 'RECLAMOS'
    data.loc[data['CODIGO'].str.contains("AN"), 'ORIGEN'] = 'ANOMALIAS'
    data.loc[data['CODIGO'].str.contains("AT"), 'ORIGEN'] = 'ANOM FACTURACION'
    logging.info('Field ORIGEN processed')
    # DESCRIPCION
    data['DESCRIPCION'] = data['ANOMALIA_REPORTADA']
    logging.info('Field DESCRIPCION added')
    # proceso: LECTURA
    data = data.assign(PROCESO='LECTURA')
    logging.info('Field PROCESO processed')
    # PENULTIMA LECTURA
    data = data.assign(PENULTIMA_LECTURA=0)
    logging.info('Field PENULTIMA_LECTURA added')
    # TIPOEQUIPO
    data = data.assign(TIPOEQUIPO='NULL')
    logging.info('Field TIPOEQUIPO added')
    # lat-lon & delegacion: from db
    fincas = pd.read_csv(
        'db/fincas.txt', delimiter=',', keep_default_na=False)
    fincas = fincas[['NIF', 'LAT', 'LON', 'DELEGACION']]
    data = pd.merge(
        data, fincas, on=['NIF'], left_index=False, right_index=False,
        sort=False, how='inner')
    data = data[data['DELEGACION'] != '']
    data.rename(columns={'LAT': 'LATITUD', 'LON': 'LONGITUD'}, inplace=True)
    logging.info('Added LAT, LON and DELEGACION fields')
    # filtrar cabeceras: corregimiento == municipio
    data = data[data['CORREGIMIENTO'] == data['MUNICIPIO']]
    logging.info('Cabeceras filter')
    # unificar fincas
    _, pnif = np.unique(data.NIF, return_index=True)
    data = data.iloc[pnif, :]
    logging.info('unique NIF filter')
    # asociado comercial: by unicom groups
    data = data.assign(ASOCIADO_COMERCIAL='')
    asociados = cfg.asociado_comercial.keys()
    for asc in asociados:
        data.loc[data['DELEGACION'].isin(cfg.asociado_comercial[asc]),
                 'ASOCIADO_COMERCIAL'] = asc
    logging.info('Field ASOCIADO_COMERCIAL processed')
    # delete ',' from NOM_CLIENTE
    data['NOM_CLIENTE'] = data['NOM_CLIENTE'].str.replace(',', ' ')
    logging.info('NOM_CLIENTE processed')
    # ordenar columnnas
    data = data[cfg.column_order]
    logging.info('Columns sorted')
    # TODO: put all parameters in the config file
    return data


def universe_generation(data, cfg):
    # TODO: save results in db
    # delete folder
    pname = 'db/results/'
    delete_folder(pname)
    # process by delegacion
    mdel = np.unique(data.DELEGACION)
    for udel in mdel:
        wd = cfg.wd
        ud = cfg.ud
        dd = data[data['DELEGACION'] == udel]
        # wd & ud validation
        if len(dd) < wd*ud:
            ud = int(np.floor(len(dd)/wd))
        # ini
        dd = dd.assign(DIA=np.zeros(len(dd)))
        cx = dd.LONGITUD.values
        cy = dd.LATITUD.values
        # day cluster
        workday = day_cluster(cx, cy, wd)
        # selection
        dd = selection(dd, workday, wd, ud)
        universe = dd[dd['DIA'] > 0].sort_values('DIA')
        # export universe
        universe.to_csv(
            pname + udel + '.txt',
            sep='\t', index=False)
        logging.info('Universe generated to ' + udel)


def send_report(cfg):
    # TODO: add a table summary by delegacion
    # email to
    emailto = cfg.emailto[0]
    for i in cfg.emailto[1:]:
        emailto = emailto + '; ' + i
    cfg.emailto = emailto
    # add attachments
    fpath = os.getcwd()
    files = glob.glob('db/results/*.txt')
    for fname in files:
        cfg.email_attachments.append(fpath + '/' + fname)
    # modify html message
    cfg.html_message = cfg.html_message.format(cfg.report_message)
    # send email
    send_email(cfg)
    logging.info('Report sended by email to ' + cfg.emailto)


def get_error_message():
    # error message
    exc_type = sys.exc_info()[0]
    exc_value = sys.exc_info()[1]
    exc_traceback = sys.exc_info()[2]
    error_message = """
        Exception Detected:
        type: {} 
        message: {} 
        file: {} 
        line: {}
    """.format(
        exc_type.__name__,
        exc_value.args[0],
        exc_traceback.tb_frame.f_code.co_filename,
        exc_traceback.tb_lineno
    )
    del(exc_type, exc_value, exc_traceback)
    logging.error(error_message)
    return error_message


def send_error(cfg):
    error_message = get_error_message()
    cfg.emailto = cfg.error_emailto
    # modify html body
    cfg.html_message = cfg.html_message.format(cfg.error_message)
    # add log file
    fpath = os.getcwd()
    lfiles = sorted(glob.glob('logs/*.log'))
    cfg.email_attachments = fpath + '/' + lfiles[-1]
    send_email(cfg)
    logging.info('Error sended by email to ' + cfg.emailto)


def send_email(cfg):
    outlook = win32.Dispatch('outlook.application')
    mail = outlook.CreateItem(0)
    mail.To = cfg.emailto
    mail.Subject = cfg.email_subject
    mail.HTMLBody = cfg.html_message
    for attachment in cfg.email_attachments:
        mail.Attachments.Add(attachment)
    mail.Display (False)
    mail.Send()


def delete_folder(pname):
    files = glob.glob(pname + '*.txt')
    for f in files:
        os.remove(f)


def day_cluster(x, y, wd):
    ki = np.floor(len(x)/wd)
    newday = np.zeros(len(x))
    for i in range(wd):
        # max pos
        ind = np.where(newday == 0)[0]
        cx = np.median(x[ind])
        cy = np.median(y[ind])
        dist = np.sqrt((x[ind] - cx)**2 + (y[ind] - cy)**2)
        xmax = x[ind[dist.argmax()]]
        ymax = y[ind[dist.argmax()]]
        # day group
        xi = x[ind]
        yi = y[ind]
        dist = np.sqrt((xi - xmax)**2 + (yi - ymax)**2)
        pos = np.argsort(dist)
        ind = ind[pos]
        if len(ind) >= ki:
            pk = ind[:int(ki)]
        else:
            pk = ind
        newday[pk] = i + 1
    return newday


def selection(data, workday, wd, ud):
    for i in range(wd):
        pw = np.where(workday == i+1)[0]
        # random selection
        rpos = np.random.choice(len(pw), ud, replace=False)
        data.DIA.values[pw[rpos]] = i + 1
    return data
