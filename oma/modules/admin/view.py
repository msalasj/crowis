
from bokeh.layouts import layout
from bokeh.models import HoverTool, DatetimeTickFormatter, NumeralTickFormatter, \
    ColumnDataSource, Circle, Range1d
from bokeh.models.widgets import Div, Select, Dropdown, TextInput, Button, DataTable, TableColumn
from bokeh.plotting import figure, curdoc

from modules.admin.controller import Controller


def create_module(user):
    # start controller
    controller = Controller(user)
    # module
    user_admin = create_user_admin(controller)
    itin_admin = create_itin_admin(controller)
    # dashboard
    dashboard = layout([
        [user_admin],
        [itin_admin]
    ], sizing_mode='fixed')
    dashboard.name = 'admin'
    # ini module data
    curdoc().add_root(dashboard)
    controller.user_selected_callback(None, None, controller.users.user.values[0])


def create_hover(sw):
    if sw == 1:
        hover = HoverTool(
            tooltips="""
                <div>
                    <div>
                        <span style="font-size: 10px; color: #505050;"> @x{%a %d %b} </span>
                    </div>
                    <div>
                        <span style="font-size: 10px; color: #505050;"> @y </span>
                    </div>
                </div>
            """,
            formatters={"x": "datetime"}
        )
    return hover


def create_user_admin(controller):
    title = Div(text='Administración de Usuarios', css_classes=['admin_title'])
    user = TextInput(title="Usuario:", css_classes=['admin_user'], name='user')
    password = TextInput(title="Contraseña:", css_classes=['admin_password'],
                         name='password')
    name = TextInput(title="Nombre:", css_classes=['admin_name'], name='name')
    email = TextInput(title="Email:", css_classes=['admin_email'], name='email')
    profile = Select(title="Perfil:", value='consulta', name='profile',
                     options=['admin', 'analista', 'consulta'],
                     css_classes=['admin_profile'])
    users = list(controller.users.user)
    user_list = Select(title="Lista de Usuarios:", value=users[0], options=users,
                       css_classes=['admin_user_list'], name='user_list')
    user_list.on_change('value', controller.user_selected_callback)
    save_button = Button(label='Guardar', button_type="primary",
                         css_classes=['admin_save_button'])
    save_button.on_click(controller.save_callback)
    delete_button = Button(label='Eliminar', button_type="primary",
                           css_classes=['admin_delete_button'])
    delete_button.on_click(controller.delete_callback)
    widget = layout([
        [title],
        [user_list, layout([
            [user, password],
            [name, email],
            [profile],
            [save_button, delete_button]
        ], sizing_mode='fixed')]
    ], sizing_mode='fixed')
    return widget


def create_itin_admin(controller):
    title = Div(text='Administración de Itinerarios', css_classes=['admin_title'])
    x = (controller.itins.latitud == 0).sum()
    text = "<b>Itinerarios sin Georeferenciación: </b> {}".format(x)
    text1 = Div(text=text, css_classes=['admin_subtitle'], name='text1')
    x = (controller.itins.clientes == 0).sum()
    text = "<b>Itinerarios sin Información: </b> {}".format(x)
    text2 = Div(text=text, css_classes=['admin_subtitle'], name='text2')
    data = controller.itins[(controller.itins.latitud == 0) |
                            (controller.itins.clientes == 0)]
    source = ColumnDataSource(data.to_dict('list'))
    columns = [
        TableColumn(field="cod_unicom", title="COD_UNICOM"),
        TableColumn(field="ruta", title="RUTA"),
        TableColumn(field="num_itin", title="NUM_ITIN"),
        TableColumn(field="tipo1", title="TIPO1"),
        TableColumn(field="tipo2", title="TIPO2"),
        TableColumn(field="tarifa", title="TARIFA"),
        TableColumn(field="cod_local", title="COD_LOCAL"),
        TableColumn(field="latitud", title="LATITUD"),
        TableColumn(field="longitud", title="LONGITUD"),
        TableColumn(field="clientes", title="CLIENTES"),
        TableColumn(field="consumo", title="CONSUMO"),
        TableColumn(field="pcobro", title="IMPORTE"),
    ]
    table = DataTable(source=source, columns=columns, width=800, height=400)
    widget = layout([
        [title],
        [text1],
        [text2],
        [table],
    ], sizing_mode='fixed')
    return widget
