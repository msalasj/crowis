
from bokeh.plotting import curdoc
from datetime import datetime

import numpy as np
import os
import pandas as pd
import pickle
import random
import sqlite3
import time


class Controller(object):

    def __init__(self, user):
        self.appname = __file__.split(os.sep)[-4]
        self.conn = sqlite3.connect(self.appname + '/data/oma.db')
        self.user = user
        self.fechas_itin = type('', (), {})()
        self.info_itin = type('', (), {})()
        self.ini_year = 0
        self.end_year = 0
        self.xrange = 0.0
        colors = pickle.load(open(self.appname + '/data/colors.p', 'rb'))
        self.day_colors = random.sample(colors, 31)
        # periodos
        self.now = datetime.now()
        self.periodo_num = self.now.month
        self.periodos_tm = np.zeros(12)
        self.periodos_str = []
        for i in range(12):
            date = datetime(year=self.now.year, month=i + 1, day=1)
            self.periodos_tm[i] = date.timestamp()
            self.periodos_str.append(date.strftime('%m-%Y'))

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.close()

    def get_user_data(self):
        self.ini_year = datetime(year=self.now.year - 1, month=12, day=1).timestamp()
        self.end_year = datetime(year=self.now.year, month=12, day=31).timestamp()
        query = "select * from fechas_itin where f_plan between {} and {}"\
            .format(self.ini_year, self.end_year)
        self.fechas_itin = pd.read_sql_query(query, self.conn)
        f99 = datetime(year=2999, month=12, day=31).timestamp()
        self.fechas_itin['f_real'].fillna(f99, inplace=True)
        self.fechas_itin['f_fact'].fillna(0, inplace=True)
        self.fechas_itin['clientes'].fillna(0, inplace=True)
        self.fechas_itin['consumo'].fillna(0, inplace=True)
        self.fechas_itin['pcobro'].fillna(0, inplace=True)
        itins = pd.read_sql_query("select * from info_itin", self.conn)
        itins = itins[itins.clientes > 0]
        geo = pd.read_sql_query("select * from geo_local", self.conn)
        self.info_itin = pd.merge(itins, geo, on='cod_local', left_index=False,
                                  right_index=False, sort=False, how='left')
        self.info_itin['municipio'].fillna('NULL', inplace=True)
        self.info_itin['delegacion'].fillna('NULL', inplace=True)
        self.info_itin['clientes'].fillna(0, inplace=True)
        self.info_itin['consumo'].fillna(0, inplace=True)
        self.info_itin['pcobro'].fillna(0, inplace=True)
        # TODO: pegar las fechas de plan y real

    def populate_menus(self, data, fechas):
        # dia
        self.populate_menu(fechas, 'menu4', 'f_plan')
        # delegaciones
        self.populate_menu(data, 'menu2', 'delegacion')
        # tipo1
        self.populate_menu(data, 'menu3', 'cod_unicom')
        # municipio
        self.populate_menu(data, 'menu5', 'municipio')
        # tipo2
        self.populate_menu(data, 'menu6', 'tipo2')

    def on_change_menus(self, attr, old, new):
        itins, fechas, mdf, mdf_real, hdias, tp, tr, fd = self.filter_data()
        # cantidad de clientes plan
        groups = fechas[['f_plan', 'clientes_plan']].groupby('f_plan').sum()
        line = curdoc().get_model_by_name('line1')
        line.data_source.data = dict(
            x=list(1000 * groups.index), y=groups.clientes_plan.values)
        # domingos
        vbar = curdoc().get_model_by_name('vbar2')
        vbar.data_source.data = dict(
            x=fd, top=np.max(groups.clientes_plan.values) * np.ones(len(fd))
        )
        # cantidad de clientes real
        groups = fechas[fechas.f_real < time.time()][['f_real', 'clientes_plan']].groupby('f_real').sum()
        line = curdoc().get_model_by_name('line1.2')
        line.data_source.data = dict(
            x=list(1000 * groups.index), y=groups.clientes_plan.values)
        # cantidad de itinerarios plan
        groups = fechas[['f_plan']].groupby('f_plan').size()
        line = curdoc().get_model_by_name('line2')
        line.data_source.data = dict(
            x=list(1000 * groups.keys()), y=groups.values)
        # domingos
        vbar = curdoc().get_model_by_name('vbar3')
        vbar.data_source.data = dict(
            x=fd, top=np.max(groups.values) * np.ones(len(fd))
        )
        # cantidad itin real
        groups = fechas[fechas.f_real < time.time()][['f_real']].groupby('f_real').size()
        line = curdoc().get_model_by_name('line2.2')
        line.data_source.data = dict(
            x=list(1000 * groups.keys()), y=groups.values)
        # geo map
        itins = itins[itins.latitud > 0]
        itins = self.filter_data_by_day(itins)
        circles = curdoc().get_model_by_name('circles1')
        x = itins.longitud.values
        y = itins.latitud.values
        z = itins.clientes.values
        sizes = 1 + 30 * z / np.max(z)
        pos = [datetime.fromtimestamp(x).day for x in itins.f_plan.values]
        if len(pos) > 1:
            colors = [self.day_colors[int(x)] for x in pos]
        else:
            colors = self.day_colors[int(pos)]
        circles.data_source.data = dict(
            lon=x, lat=y, sizes=sizes, colors=colors,
            cod_unicom=itins.cod_unicom.values,
            ruta=itins.ruta.values,
            itin=itins.num_itin.values
        )
        fmap = curdoc().get_model_by_name('fig3')
        fmap.map_options.lng = (x.max() + x.min()) / 2
        fmap.map_options.lat = (y.max() + y.min()) / 2
        zoom = 7
        if self.xrange == 0:
            self.xrange = np.abs(x.max() - x.min())
        if len(x) > 1:
            zoom = zoom + int(np.log2(self.xrange / np.abs(x.max() - x.min())))
        else:
            zoom = zoom
        fmap.map_options.zoom = zoom
        # Promedio de dias facturados plan
        line = curdoc().get_model_by_name('line4')
        line.data_source.data = dict(x=np.arange(1, 13), y=mdf)
        # dias facturados real
        line = curdoc().get_model_by_name('line4.2')
        pk = np.where(mdf_real > 0)[0]
        line.data_source.data = dict(x=np.arange(1, 13)[pk], y=mdf_real[pk])
        # histograma de dias facturados
        hist, edges = np.histogram(hdias['plan'], np.unique(hdias['plan']).astype(int))
        vbar = curdoc().get_model_by_name('vbar1')
        vbar.data_source.data = dict(x=edges[:-1], top=hist, y=hist)
        # histograma real
        line = curdoc().get_model_by_name('line5.2')
        if len(hdias['real']) > 0:
            hist, edges = np.histogram(hdias['real'], np.unique(hdias['real']).astype(int))
            line.data_source.data = dict(x=edges[:-1], y=hist)
        else:
            x = np.unique(hdias['plan'])
            y = np.zeros(len(y))
            line.data_source.data = dict(x=x, y=y)
        # traslados plan
        typeg = curdoc().get_model_by_name('button_group1').active
        line = curdoc().get_model_by_name('line6')
        line.data_source.data = dict(x=np.arange(1, 13), y=tp[:, typeg])
        # traslados real
        line = curdoc().get_model_by_name('line6.2')
        y = tr[:, typeg]
        pk = np.where(y > 0)[0]
        line.data_source.data = dict(x=np.arange(1, 13)[pk], y=y[pk])

    def filter_data(self):
        # filter itins
        itins = self.info_itin
        menus = ['menu2', 'menu3', 'menu5', 'menu6']
        field = ['delegacion', 'cod_unicom', 'municipio', 'tipo2']
        for i in range(len(menus)):
            value = curdoc().get_model_by_name(menus[i]).value
            if value != 'TODOS':
                if field[i] == 'cod_unicom':
                    value = int(value)
                itins = itins[itins[field[i]] == value]
        # periodo filter
        fechas = self.fechas_itin
        options = curdoc().get_model_by_name('menu1').options
        value = curdoc().get_model_by_name('menu1').value
        self.periodo_num = options.index(value)
        pk = options.index(value)
        ini_lim = self.periodos_tm[pk]
        if pk < 11:
            end_lim = self.periodos_tm[pk + 1] - 3600 * 24
        else:
            end_lim = self.periodos_tm[pk] + 3600 * 24 * 30
        fechas = fechas[(fechas.f_plan >= ini_lim) &
                        (fechas.f_plan <= end_lim)]
        # Domingos
        x = datetime.fromtimestamp(ini_lim)
        ini_date = datetime(year=x.year, month=x.month, day=1)
        fmes = pd.date_range(start=ini_date, periods=30, freq='1D')
        dias = np.array([x.weekday() for x in fmes])
        dpos = np.where(dias == 6)[0]
        fd = np.zeros(len(dpos))
        for i in range(len(dpos)):
            fd[i] = 1000 * fmes[dpos[i]].timestamp()
        # from itins to fechas
        base = itins[['cod_unicom', 'ruta', 'num_itin', 'clientes',
                      'consumo', 'pcobro']]
        base.columns = ['cod_unicom', 'ruta', 'num_itin', 'clientes_plan',
                        'consumo_plan', 'pcobro_plan']
        fechas = pd.merge(fechas, base, on=['cod_unicom', 'ruta', 'num_itin'],
                          how='inner')
        fechas = fechas[fechas.clientes_plan > 0]
        # from fechas to itin
        base = fechas[['cod_unicom', 'ruta', 'num_itin', 'f_plan']]
        itins = pd.merge(itins, base, on=['cod_unicom', 'ruta', 'num_itin'],
                         how='inner')
        # plan data
        # TODO: mejorar la manera de calcular la base de planificacion
        # dias facturados
        mdf, mdf_real, hdias = self.get_dias_facturados(itins)
        # tralados
        tp, tr = self.get_traslados(itins)
        # TODO: no recalcular los dias facturados ni los traslados si estos no cambian.
        # TODO: calcularlos al principio, guardarlos en Controller y luego filtrar.
        # TODO: esto deberia ya estar calculado en base de datos.
        # TODO: la herramienta solo deberia procesar filtros.
        # update menus
        self.populate_menus(itins, fechas)
        return itins, fechas, mdf, mdf_real, hdias, tp, tr, fd

    def populate_menu(self, data, model_name, fname):
        menu = curdoc().get_model_by_name(model_name)
        menu.disabled = True
        cvalue = menu.value
        if fname == 'f_plan':
            items = self.get_dias(data)
            if (cvalue not in items) | (cvalue == 'TODOS'):
                items.insert(0, 'TODOS')
                menu.options = items
                menu.value = items[0]
        else:
            if cvalue == 'TODOS':
                items = list(np.unique(data[fname]))
                if fname == 'cod_unicom':
                    items = list(map(str, items))
                items.insert(0, 'TODOS')
                menu.options = items
                menu.value = items[0]
            else:
                items = ['TODOS', cvalue]
                menu.options = items
                menu.value = items[1]
        menu.disabled = False

    @staticmethod
    def get_dias(data):
        dias = np.unique(data.f_plan)
        strday = []
        for i in range(len(dias)):
            strday.append(datetime.fromtimestamp(dias[i]).strftime('%d-%m-%Y'))
        return strday

    @staticmethod
    def filter_data_by_day(data):
        strday = curdoc().get_model_by_name('menu4').value
        if strday != 'TODOS':
            date = [int(x) for x in strday.split('-')]
            dia = datetime(year=date[2], month=date[1],
                           day=date[0]).timestamp()
            data = data[data.f_plan == dia]
        return data

    def get_dias_facturados(self, itins):
        mdf = np.zeros(12)
        mdf_real = np.zeros(12)
        base = itins[['cod_unicom', 'ruta', 'num_itin']]
        data = self.fechas_itin
        today = time.time()
        # data = data.groupby(['cod_unicom', 'ruta', 'num_itin'])
        periodos = np.unique(data.periodo)
        data0 = data[data.periodo == periodos[0]]
        iii = pd.merge(base, data0, on=['cod_unicom', 'ruta', 'num_itin'],
                       how='inner')
        fechas = np.zeros([len(itins), 4])
        fechas[:, 0] = iii.f_plan.values
        fechas[:, 2] = iii.f_real.values
        for i in range(1, len(periodos)):
            datai = data[data.periodo == periodos[i]]
            iii = pd.merge(base, datai, on=['cod_unicom', 'ruta', 'num_itin'],
                           how='inner')
            fechas[:, 1] = iii.f_plan.values
            fechas[:, 3] = iii.f_real.values
            d1 = (fechas[:, 1] - fechas[:, 0]) / (3600 * 24)
            mdf[i - 1] = np.mean(d1)
            pk = np.where((fechas[:, 2] < today) & (fechas[:, 3] < today))[0]
            d2 = (fechas[pk, 3] - fechas[pk, 2]) / (3600 * 24)
            if len(pk) > 0:
                mdf_real[i - 1] = np.mean(d2)
            fechas[:, 0] = fechas[:, 1]
            fechas[:, 2] = fechas[:, 3]
            # histogramas
            if i == (self.periodo_num + 1):
                hdias = {'plan': d1, 'real': d2}
        return mdf, mdf_real, hdias

    def get_traslados(self, itins):
        fechas = self.fechas_itin
        base = itins[['cod_unicom', 'ruta', 'num_itin',
                      'consumo', 'pcobro']]
        base.columns = ['cod_unicom', 'ruta', 'num_itin',
                        'consumo_plan', 'pcobro_plan']
        fechas = pd.merge(fechas, base, on=['cod_unicom', 'ruta', 'num_itin'],
                          how='inner')
        data = np.zeros([12, 3])
        datar = np.zeros([12, 3])
        venc = np.array([24, 21, 21, 23, 24, 22, 24, 24, 21, 24, 23, 21])
        meses = np.array([datetime.fromtimestamp(x).month
                          for x in fechas.f_plan.values])
        dias = np.array([datetime.fromtimestamp(x).day for x in fechas.f_plan.values])
        mesesr = np.array([datetime.fromtimestamp(x).month
                          for x in fechas.f_real.values])
        diasr = np.array([datetime.fromtimestamp(x).day for x in fechas.f_real.values])
        consumos = fechas.consumo_plan.values
        pcobro = fechas.pcobro_plan.values
        for i in range(12):
            # plan
            pk = np.where((meses == i + 1) & (dias > venc[i]))[0]
            data[i, :] = [len(pk), np.sum(consumos[pk]), np.sum(pcobro[pk])]
            # real
            if i <= (self.now.month - 1):
                pk = np.where((mesesr == i + 1) & (diasr > venc[i]))[0]
                datar[i, :] = [len(pk), np.sum(consumos[pk]), np.sum(pcobro[pk])]
        return data, datar
