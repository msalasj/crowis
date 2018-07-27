
from bokeh.plotting import curdoc

import os
import pandas as pd
import sqlite3


class Controller(object):

    def __init__(self, user):
        self.appname = __file__.split(os.sep)[-4]
        self.conn = sqlite3.connect(self.appname + '/data/oma.db')
        self.users = pd.read_sql_query("select * from usuarios", self.conn)
        self.users = self.users[self.users.user != 'jonate']
        self.user = user
        self.itins = pd.read_sql_query("select * from info_itin", self.conn)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.close()

    def user_selected_callback(self, attr, old, new):
        info = self.users[self.users.user == new]
        model_names = list(self.users.columns)
        for name in model_names:
            model = curdoc().get_model_by_name(name)
            model.value = info[name].values[0]

    def save_callback(self):
        # validate new user
        user_list = list(self.users.user)
        user = curdoc().get_model_by_name('user').value
        if user:
            model_names = list(self.users.columns)
            values = [curdoc().get_model_by_name(name).value
                      for name in model_names]
            if user in user_list:
                # update
                query = "update usuarios set password='{}', name='{}'," \
                        "email='{}', profile='{}' where user='{}'".format(
                            values[1], values[2], values[3], values[4],
                            values[0]
                        )
            else:
                # create new entry
                query = "insert into usuarios values(" \
                        "'{}','{}','{}','{}','{}')".format(
                            values[0], values[1], values[2], values[3],
                            values[4]
                        )
            self.conn.execute(query)
            self.conn.commit()
            self.update_users()

    def delete_callback(self):
        user_list = list(self.users.user)
        user = curdoc().get_model_by_name('user').value
        if user in user_list:
            query = "delete from usuarios where user='{}'".format(user)
            self.conn.execute(query)
            self.conn.commit()
            self.update_users()

    def update_users(self):
        self.users = pd.read_sql_query("select * from usuarios", self.conn)
        self.users = self.users[self.users.user != 'jonate']
        model = curdoc().get_model_by_name('user_list')
        model.options = list(self.users.user)
        model.value = self.users.user.values[0]
        self.user_selected_callback(None, None, model.value)

