
from bokeh.layouts import layout
from bokeh.models import Range1d
from bokeh.models.widgets import Button, Div, TextInput, PasswordInput
from bokeh.plotting import figure, curdoc

from modules.login.controller import Controller


def create_module():
    # start controller
    controller = Controller()
    # im logo
    logo = figure()
    logo = config_fig_logo(logo, controller.appname)
    logo.css_classes = ['login_logo']
    # title1
    title1 = Div(text='Optimización y Mantenimiento de la Agenda',
                 css_classes=['login_title1'])
    line = Div(text='_'*50, css_classes=['login_line'])
    # title2
    title2 = Div(text='Control de Acceso', css_classes=['login_title2'])
    validation = Div(text='', css_classes=['login_validation'],
                     name='login.validation')
    # edits
    user = TextInput(title="Usuario:",
                     css_classes=['login_user'], name='login.user')
    password = PasswordInput(css_classes=['login_password'],
                             name='login.password', width=420,
                             title='Contraseña:')
    # button
    button_go = Button(
        label='Ingresar', button_type="primary",
        css_classes=['login_button_go'])
    button_go.on_click(controller.access_control)
    # dashboard
    login = layout(
        [
            [logo],
            [title1],
            [line],
            [title2],
            [validation],
            [user],
            [password],
            [button_go]
        ],
        sizing_mode='fixed',
    )
    login.name = 'login'
    curdoc().add_root(login)
    curdoc().title = 'OMA'


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
