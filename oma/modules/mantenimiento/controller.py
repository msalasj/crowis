
from bokeh.plotting import curdoc
from datetime import datetime

import math
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
        # itins
        itins = pd.read_sql_query("select * from info_itin", self.conn)
        itins = itins[itins.clientes > 0]
        geo = pd.read_sql_query("select * from geo_local", self.conn)
        self.itins = pd.merge(itins, geo, on='cod_local', left_index=False,
                              right_index=False, sort=False, how='inner')
        self.itins['municipio'].fillna('NULL', inplace=True)
        self.itins['delegacion'].fillna('NULL', inplace=True)
        self.itins['corregimiento'].fillna('NULL', inplace=True)
        self.itins['clientes'].fillna(0, inplace=True)
        self.itins['consumo'].fillna(0, inplace=True)
        self.itins['pcobro'].fillna(0, inplace=True)
        self.witins = self.itins
        # add fechas
        self.now = datetime.now()
        self.ini_year = datetime(year=self.now.year-1, month=12, day=1).timestamp()
        self.end_year = datetime(year=self.now.year, month=12, day=31).timestamp()
        query = "select * from fechas_itin where f_plan between {} and {}"\
            .format(self.ini_year, self.end_year)
        self.fechas = pd.read_sql_query(query, self.conn)
        f99 = datetime(year=2999, month=12, day=31).timestamp()
        self.fechas['f_real'].fillna(f99, inplace=True)
        self.fechas['f_fact'].fillna(0, inplace=True)
        self.fechas['clientes'].fillna(0, inplace=True)
        self.fechas['consumo'].fillna(0, inplace=True)
        self.fechas['pcobro'].fillna(0, inplace=True)
        # dias
        self.dias = []
        # colors
        colors = pickle.load(open(self.appname + '/data/colors.p', 'rb'))
        self.day_colors = random.sample(colors, 31)
        self.xrange = 0.0

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.close()

    def on_change_menus(self, attr, old, new):
        itins = self.filter_data()
        self.witins = itins
        # populate menus
        self.populate_menus(itins)
        # update plots
        self.update_plots(itins, itins.dialect.values,
                          self.dias[:, 0], self.dias[:, 2], self.dias[:, 1])

    def filter_data(self):
        # filter itins
        itins = self.itins
        menus = ['menu1', 'menu2', 'menu3', 'menu4', 'menu5']
        field = ['delegacion', 'cod_unicom', 'municipio', 'corregimiento', 'tipo2']
        for i in range(len(menus)):
            value = curdoc().get_model_by_name(menus[i]).value
            if value != 'TODOS':
                if field[i] == 'cod_unicom':
                    value = int(value)
                itins = itins[itins[field[i]] == value]
        # add fechas
        periodo = int(datetime(year=self.now.year, month=self.now.month,
                               day=1).strftime('%Y%m'))
        fechas = self.fechas[self.fechas.periodo == periodo]
        base = fechas[['cod_unicom', 'ruta', 'num_itin', 'f_plan']]
        itins = pd.merge(itins, base, on=['cod_unicom', 'ruta', 'num_itin'],
                         how='inner')
        # filters
        itins = itins[itins.clientes > 0]
        # dias
        dias = np.unique(itins.f_plan)
        self.dias = np.zeros([len(dias), 4])
        itins['dialect'] = np.zeros(len(itins))
        for i in range(len(dias)):
            # dia
            self.dias[i, 0] = i + 1
            itins['dialect'].values[itins.f_plan == dias[i]] = i + 1
            # cantidad de itinerarios
            self.dias[i, 1] = np.sum(itins.f_plan == dias[i])
            # cantidad de clientes
            self.dias[i, 2] = np.sum(itins.clientes[itins.f_plan == dias[i]])
            # day date
            self.dias[i, 3] = dias[i]
        return itins

    @staticmethod
    def populate_menus(data):
        menus = ['menu1', 'menu2', 'menu3', 'menu4', 'menu5']
        field = ['delegacion', 'cod_unicom', 'municipio', 'corregimiento', 'tipo2']
        for i in range(len(menus)):
            menu = curdoc().get_model_by_name(menus[i])
            menu.disabled = True
            cvalue = menu.value
            fname = field[i]
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

    def update_plots(self, data, dialect, dias, cxd, ixd):
        # metrics
        nd = len(dias)
        # cantidad de clientes
        model = curdoc().get_model_by_name('vbar1')
        model.data_source.data = dict(x=dias, top=cxd, y=cxd)
        m1 = [np.mean(cxd)]
        model = curdoc().get_model_by_name('line1.2')
        model.data_source.data = dict(x=dias, y=m1*nd)
        # cantidad de itinerarios
        model = curdoc().get_model_by_name('vbar2')
        model.data_source.data = dict(x=dias, top=ixd, y=ixd)
        m2 = [np.mean(ixd)]
        model = curdoc().get_model_by_name('line2.2')
        model.data_source.data = dict(x=dias, y=m2*nd)
        # mapa
        pk = (data.latitud.values > 0) & (dialect > 0)
        itins = data.iloc[pk]
        dialect = dialect[pk]
        circles = curdoc().get_model_by_name('circles1')
        x = itins.longitud.values
        y = itins.latitud.values
        z = itins.clientes.values
        sizes = 1 + 30*z/np.max(z)
        if len(dialect) > 1:
            colors = [self.day_colors[int(x)] for x in dialect]
        else:
            colors = [self.day_colors[int(dialect)]]
        circles.data_source.data = dict(
            lon=x, lat=y, sizes=sizes, colors=colors,
            cod_unicom=itins.cod_unicom.values,
            ruta=itins.ruta.values,
            itin=itins.num_itin.values
        )
        fmap = curdoc().get_model_by_name('fig3')
        fmap.map_options.lng = (x.max() + x.min())/2
        fmap.map_options.lat = (y.max() + y.min())/2
        zoom = 7
        if self.xrange == 0:
            self.xrange = np.abs(x.max() - x.min())
        if len(x) > 1:
            zoom = zoom + int(np.log2(self.xrange/np.abs(x.max() - x.min())))
        else:
            zoom = zoom
        fmap.map_options.zoom = zoom
        # distacia entre itinerarios
        model = curdoc().get_model_by_name('vbar4')
        y = self.get_day_distances(itins, dialect, nd)
        model.data_source.data = dict(x=dias, top=y, y=y)

    def get_day_distances(self, itins, dialect, nd):
        day_dist = np.zeros(nd)
        for i in range(nd):
            datai = itins[dialect == i+1]
            if len(datai) > 1:
                x = datai.longitud.values
                y = datai.latitud.values
                cx = np.median(x)
                cy = np.median(y)
                dist = np.zeros(len(x))
                for j in range(len(x)):
                    dist[j] = self.geo_distance(cy, cx, y[j], x[j])
                day_dist[i] = np.mean(dist)
        return day_dist

    @staticmethod
    def geo_distance(lat1, lon1, lat2, lon2):
        r = 6371.0
        dlat = math.radians(lat2 - lat1)
        dlon = math.radians(lon2 - lon1)
        a = math.sin(dlat / 2)**2 + math.cos(math.radians(lat1)) * \
            math.cos(math.radians(lat2)) * math.sin(dlon / 2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        distance = r * c
        return distance

    def optim_days(self):
        data = self.witins
        dias = self.dias
        w1, w2, w3, werr, simulate = self.get_parameters()
        # Premisa # 1: previamente selección el universo objetivo
        # Premisa # 2: el número de días son los previamente planificados
        # parameters
        lat = data.latitud.values
        lon = data.longitud.values
        clientes = data.clientes.values
        fplan = data.f_plan.values
        nd = len(dias)
        weights = [w1, w2, w3]
        # plan day
        planday = np.zeros(len(lat))
        cxd = np.zeros(nd)
        ixd = np.zeros(nd)
        for i in range(nd):
            pos = fplan == dias[i, 3]
            planday[pos] = dias[i, 0]
            pos = (fplan == dias[i, 3]) & (lat == 0)
            cxd[i] = np.sum(clientes[pos])
            ixd[i] = sum(pos)
        # criterios de optimización
        swc = np.sum(clientes)/nd
        swi = round(len(clientes)/nd)
        pkih = 1 + werr  # 3% de error
        pkil = 1 - werr
        kpic = np.round([pkil*swc, pkih*swc])
        ik = np.ceil(werr*swi)
        kpii = [swi-ik, swi+ik]
        newday = np.zeros(len(lat))
        # models to update
        vbar5 = curdoc().get_model_by_name('vbar5')
        for i in range(nd):
            # ini
            dia = i + 1
            nc = cxd[i]
            ni = ixd[i]
            newday[(planday == dia) & (lat == 0)] = dia
            pi = (planday == dia) & (lat > 0)
            xi = np.median(pi)
            yi = np.median(pi)
            val1 = True
            while val1:
                pij = (newday == 0) & (lat > 0)
                ind = np.where(pij)[0]
                # criterios
                cri = np.zeros([len(ind), 3])
                cri[:, 0] = self.normalize_zo(np.abs(swc - nc - clientes[pij]))
                cri[:, 1] = self.normalize_zo(np.abs(dia - planday[pij]))
                dist = np.sqrt((lon[pij] - xi)**2 + (lat[pij] - yi)**2)
                cri[:, 2] = self.normalize_zo(dist)
                # evaluación
                ivalue = np.average(cri, axis=1, weights=weights)
                # selección
                val2 = True
                continuar = True
                while val2:
                    pmin = ivalue.argmin()
                    if ivalue.min() < 1:
                        if nc + clientes[ind[pmin]] <= kpic[1]:
                            val2 = False
                            newday[ind[pmin]] = dia
                            nc = nc + clientes[ind[pmin]]
                            ni += 1
                            # update plots
                            if simulate:
                                # movimientos
                                pk = newday > 0
                                m = newday[pk] - planday[pk]
                                bins = np.unique(m)
                                bins = np.append(bins, bins[-1]+1)
                                h, _ = np.histogram(m, bins)
                                vbar5.data_source.data = dict(x=np.unique(m), top=h, y=h)
                                # plots
                                cxd[i] = nc
                                ixd[i] = ni
                                self.update_plots(data, newday, dias[:, 0], cxd, ixd)
                                time.sleep(1)
                        else:
                            ivalue[pmin] = 1
                    else:
                        val2 = False
                        continuar = False
                # validacion
                if (not continuar) | (ni + 1 > kpii[1]) | \
                        ((ni >= kpii[0]) & (nc >= kpic[0])):
                    val1 = False
            # save results
            cxd[i] = nc
            ixd[i] = ni
        # itins faltantes:
        print('Limits: {}, {}'.format(kpii, kpic))
        print('Itins Faltantes: {} - {}'.format(sum(newday == 0), sum(clientes[newday == 0])))
        # Movimiento de Itinerarios
        m = newday - planday
        print('Total Movimientos: {}'.format(sum(np.abs(m) > 0)))
        print('Movimiento Neto: {}'.format(sum(m)))
        if not simulate:
            pk = newday > 0
            m = newday[pk] - planday[pk]
            bins = np.unique(m)
            bins = np.append(bins, bins[-1]+1)
            h, _ = np.histogram(m, bins)
            vbar5.data_source.data = dict(x=np.unique(m), top=h, y=h)
            # update plots
            self.update_plots(data, newday, dias[:, 0], cxd, ixd)

    @staticmethod
    def normalize_zo(h):
        miny = np.min(h)
        maxy = np.max(h)
        if maxy > miny:
            m = 1/(maxy - miny)
            y = m*h - m*miny
        else:
            y = 0*h
        return y

    @staticmethod
    def get_parameters():
        w1 = int(curdoc().get_model_by_name('menu7').value)
        w2 = int(curdoc().get_model_by_name('menu8').value)
        w3 = int(curdoc().get_model_by_name('menu9').value)
        werr = int(curdoc().get_model_by_name('menu6').value)/100
        simulate = False
        if curdoc().get_model_by_name('checkbox1').active:
            simulate = True
        return w1, w2, w3, werr, simulate

    def optim_days_2(self):
        data = self.witins
        dias = self.dias
        w1, w2, w3, werr, simulate = self.get_parameters()
        # input data
        lat = data.latitud.values
        lon = data.longitud.values
        clientes = data.clientes.values
        fplan = data.f_plan.values
        nd = len(dias)
        # plan day
        planday = np.zeros(len(lat))
        cxd = np.zeros(nd)
        ixd = np.zeros(nd)
        for i in range(nd):
            pos = fplan == dias[i, 3]
            planday[pos] = dias[i, 0]
            pos = (fplan == dias[i, 3]) & (lat == 0)
            cxd[i] = np.sum(clientes[pos])
            ixd[i] = sum(pos)
        # criterios de optimización
        swc = np.sum(clientes)/nd
        swi = round(len(clientes)/nd)
        pkih = 1 + werr  # 3% de error
        pkil = 1 - werr
        kpic = np.round([pkil*swc, pkih*swc])
        ik = np.ceil(werr*swi)
        kpii = [swi-ik, swi+ik]
        newday = np.zeros(len(lat))
        for i in range(nd):
            # ini
            dia = i + 1
            nc = cxd[i]
            ni = ixd[i]
            newday[(planday == dia) & (lat == 0)] = dia
            pi = (planday == dia) & (lat > 0)
            xi = np.median(pi)
            yi = np.median(pi)
            val1 = True
            while val1:
                pij = (newday == 0) & (lat > 0)
                ind = np.where(pij)[0]
                # criterios
                cri = np.zeros([len(ind), 3])
                cri[:, 0] = self.normalize_zo(np.abs(swc - nc - clientes[pij]))
                cri[:, 1] = self.normalize_zo(np.abs(dia - planday[pij]))
                dist = np.sqrt((lon[pij] - xi)**2 + (lat[pij] - yi)**2)
                cri[:, 2] = self.normalize_zo(dist)
                # evaluación
                ivalue = np.average(cri, axis=1, weights=weights)
                # selección
                val2 = True
                continuar = True
                while val2:
                    pmin = ivalue.argmin()
                    if ivalue.min() < 1:
                        if nc + clientes[ind[pmin]] <= kpic[1]:
                            val2 = False
                            newday[ind[pmin]] = dia
                            nc = nc + clientes[ind[pmin]]
                            ni += 1
                        else:
                            ivalue[pmin] = 1
                    else:
                        val2 = False
                        continuar = False
                # validacion
                if (not continuar) | (ni + 1 > kpii[1]) | \
                        ((ni >= kpii[0]) & (nc >= kpic[0])):
                    val1 = False
            # save results
            cxd[i] = nc
            ixd[i] = ni
            print('Dia {} optimizado'.format(dia))
        # itins faltantes:
        print('Limits: {}, {}'.format(kpii, kpic))
        print('Itins Faltantes: {} - {}'.format(sum(newday == 0), sum(clientes[newday == 0])))
        print(cxd)
        print(ixd)
        m = newday - planday
        print('Total Movimientos: {}'.format(sum(np.abs(m) > 0)))
        print('Movimiento Neto: {}'.format(sum(m)))
        h, _ = np.histogram(m, np.unique(m))
        print(np.unique(m))
        print(h)
