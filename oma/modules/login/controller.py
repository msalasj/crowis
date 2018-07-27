
from bokeh.plotting import curdoc

import importlib
import os
import pandas as pd
import sqlite3


class Controller(object):

    def __init__(self):
        self.appname = __file__.split(os.sep)[-4]
        self.conn = sqlite3.connect(self.appname + '/data/oma.db')
        self.user = []

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.close()

    def access_control(self):
        user = curdoc().get_model_by_name('login.user')
        password = curdoc().get_model_by_name('login.password')
        result = self.validate_user(user.value, password.value)
        if result:
            # create header panel
            view = importlib.import_module('modules.header.view')
            view.create_module(self.user)
            # create and monitoring
            view = importlib.import_module('modules.monitoring.view')
            view.create_module(self.user)
        else:
            user.value = ''
            password.value = ''
            validation = curdoc().get_model_by_name('login.validation')
            validation.text = 'Usuario y/o contraseña invalidos'

    def validate_user(self, user, password):
        user = user.strip()
        password = password.strip()
        query = "select * from usuarios"
        users = pd.read_sql_query(query, self.conn)
        users = users[(users.user == user) & (users.password == password)]
        if not users.empty:
            result = True
            self.user = users.iloc[0]
        else:
            result = False
        return result
