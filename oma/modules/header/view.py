
from bokeh.layouts import layout
from bokeh.models import Range1d
from bokeh.models.widgets import Div, Dropdown
from bokeh.plotting import curdoc, figure

from modules.header.controller import Controller


def create_module(user):
    # start controller
    controller = Controller(user)
    # header panel
    dashboard = create_panel(controller)
    # curdoc().remove_root(curdoc().roots[0])
    curdoc().clear()
    curdoc().add_root(dashboard)


def create_panel(controller):
    # im logo
    logo = figure()
    logo = config_fig_logo(logo, controller.appname)
    logo.css_classes = ['panel_logo']
    # title
    title = Div(text='Optimización y Mantenimiento de la Agenda',
                css_classes=['panel_title'], width=680)
    # modules selection
    menu = get_user_modules(controller.user.profile)
    panel_menu = Dropdown(
        label='Módulos',
        button_type="primary",
        menu=menu,
        css_classes=['panel_menu'],
        name='panel_menu',
        width=150,
    )
    panel_menu.on_click(controller.module_selection)
    # widget
    widget = layout([
        [logo, title, panel_menu]
    ], sizing_mode='fixed')
    widget.name = 'header'
    return widget


def config_fig_logo(fig, app_name):
    w = 120
    h = 15
    fig.x_range = Range1d(0, w)
    fig.y_range = Range1d(0, h)
    fig.plot_width = 300
    fig.plot_height = 100
    fig.image_url(url=[app_name + '/static/eca_logo.png'], x=0, y=0,
                  w=None, h=None, anchor='bottom_left')
    fig.toolbar.logo = None
    fig.toolbar_location = None
    fig.xaxis.visible = None
    fig.yaxis.visible = None
    fig.xgrid.grid_line_color = None
    fig.ygrid.grid_line_color = None
    fig.border_fill_color = None
    fig.outline_line_color = None
    return fig


def get_user_modules(access):
    if access == 'admin':
        menu = [
            ("Seguimiento", "monitoring"),
            ("Mantenimiento", "mantenimiento"),
            None,
            ('Administración', 'admin'),
            None,
            ('Cerrar Sesión', 'login')
        ]
    elif access == 'analista':
        menu = [
            ("Seguimiento", "monitoring"),
            ("Mantenimiento", "mantenimiento"),
            None,
            ('Cerrar Sesión', 'login')
        ]
    else:
        menu = [
            ("Seguimiento", "monitoring"),
            None,
            ('Cerrar Sesión', 'login')
        ]
    return menu
