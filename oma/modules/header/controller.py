
from bokeh.plotting import curdoc

import importlib
import os


class Controller(object):

    def __init__(self, user):
        self.appname = __file__.split(os.sep)[-4]
        self.user = user

    def module_selection(self, select):
        modules = curdoc().roots
        if len(modules) == 1:
            module = modules[0]
        else:
            module = modules[1]
        if module.name != select:
            # delete previos module
            if module.name != 'header':
                curdoc().remove_root(module)
            # create the new module
            if select == 'monitoring':
                view = importlib.import_module('modules.monitoring.view')
                view.create_module(self.user)
            elif select == 'mantenimiento':
                view = importlib.import_module('modules.mantenimiento.view')
                view.create_module(self.user)
            elif select == 'admin':
                view = importlib.import_module('modules.admin.view')
                view.create_module(self.user)
            elif select == 'login':
                curdoc().clear()
                view = importlib.import_module('modules.login.view')
                view.create_module()
