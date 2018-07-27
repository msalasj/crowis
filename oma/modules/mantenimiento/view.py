
from bokeh.layouts import layout
from bokeh.models import HoverTool, DatetimeTickFormatter, NumeralTickFormatter, \
    ColumnDataSource, Circle, Range1d, GMapPlot, GMapOptions, PanTool, WheelZoomTool, Spacer
from bokeh.models.widgets import Div, Select, TextInput, Button, RadioButtonGroup, CheckboxGroup
from bokeh.plotting import figure, curdoc

from modules.mantenimiento.controller import Controller

import numpy as np


def create_module(user):
    # start controller
    controller = Controller(user)
    # module
    # Section 1
    title1 = Div(text='Selección del Universo Objetivo', css_classes=['mtt_title'])
    menu1 = Select(title="Delegación:", value="TODOS", name='menu1',
                   options=["TODOS"], width=200, css_classes=['mtt_menu1'])

    menu2 = Select(title="Unicom:", value='TODOS', name='menu2',
                   options=['TODOS'], width=200, css_classes=['mtt_menu2'])

    menu3 = Select(title="Municipio:", value="TODOS", name='menu3',
                   options=["TODOS"], width=200, css_classes=['mtt_menu3'])

    menu4 = Select(title="Corregimiento:", value="TODOS", name='menu4',
                   options=["TODOS"],  width=200, css_classes=['mtt_menu4'])

    menu5 = Select(title="Tipología:", value="TODOS", name='menu5',
                   options=["TODOS"], width=200, css_classes=['mtt_menu5'])
    # Section 2
    title2 = Div(text='Criterios de Optimización', css_classes=['mtt_title'])

    fig1 = figure(plot_width=600, plot_height=300, css_classes=['mtt_fig1'],
                  tools='pan,box_zoom,reset', name='fig1',
                  title='Cantidad de Clientes x día de Lectura')
    fig1.toolbar.logo = None
    fig1.toolbar_location = 'above'
    fig1.vbar(x=[1, 2, 3], width=0.5, bottom=0, top=[1.2, 2.5, 3.7], color="darkcyan",
              fill_alpha=0.6, line_color='black', name='vbar1')
    fig1.line(x=[0, 1], y=[0, 1], line_color="red", line_width=2,
              alpha=0.8, legend='Promedio', name='line1.2')
    fig1.legend.click_policy = "hide"
    fig1.legend.location = "top_left"
    fig1.legend.background_fill_color = "white"
    fig1.legend.background_fill_alpha = 0.5
    fig1.legend.label_text_color = "#505050"
    fig1.legend.orientation = "vertical"
    fig1.xaxis.axis_label = 'Día de Lectura'
    fig1.add_tools(create_hover(1))
    fig1.yaxis[0].formatter = NumeralTickFormatter(format="0.0a")

    fig2 = figure(plot_width=600, plot_height=300, css_classes=['mtt_fig2'],
                  tools='pan,box_zoom,reset', name='fig2',
                  title='Cantidad de Itinerarios x día de Lectura')
    fig2.toolbar.logo = None
    fig2.toolbar_location = 'above'
    fig2.vbar(x=[1, 2, 3], width=0.5, bottom=0, top=[1.2, 2.5, 3.7], color="darkcyan",
              fill_alpha=0.6, line_color='black', name='vbar2')
    fig2.line(x=[0, 1], y=[0, 1], line_color="red", line_width=2,
              alpha=0.8, legend='Promedio', name='line2.2')
    fig2.legend.click_policy = "hide"
    fig2.legend.location = "top_left"
    fig2.legend.background_fill_color = "white"
    fig2.legend.background_fill_alpha = 0.5
    fig2.legend.label_text_color = "#505050"
    fig2.legend.orientation = "vertical"
    fig2.xaxis.axis_label = 'Día de Lectura'
    fig2.add_tools(create_hover(1))
    fig2.yaxis[0].formatter = NumeralTickFormatter(format="0.0a")

    map_options = GMapOptions(lat=10.032663, lng=-74.042470,
                              map_type="roadmap", zoom=7)
    fig3 = GMapPlot(x_range=Range1d(), y_range=Range1d(),
                    map_options=map_options,
                    plot_width=600, plot_height=450, css_classes=['mtt_fig3'],
                    name='fig3')
    fig3.toolbar.logo = None
    fig3.toolbar_location = 'above'
    fig3.add_tools(PanTool(), WheelZoomTool())
    fig3.title.text = 'Dispersión Geográfica de Itinerarios'
    fig3.api_key = 'AIzaSyATl81v4Wnm4udDvlNTcgw4oWMzWJndkfQ'
    x = np.linspace(-2, 2, 10)
    source = ColumnDataSource(
        data=dict(
            lat=x,
            lon=x**2,
            sizes=np.linspace(10, 20, 10),
            colors=controller.day_colors[0:10],
        )
    )
    circle = Circle(x="lon", y="lat", size='sizes',
                    fill_color='colors', fill_alpha=0.6, line_color='black')
    fig3.add_glyph(source, circle, name='circles1')
    fig3.add_tools(create_hover(2))

    fig4 = figure(plot_width=600, plot_height=300, css_classes=['mtt_fig4'],
                  tools='pan,box_zoom,reset', name='fig2',
                  title='Distancia Media entre Itinerarios (Km)')
    fig4.toolbar.logo = None
    fig4.toolbar_location = 'above'
    fig4.vbar(x=[1, 2, 3], width=0.5, bottom=0, top=[1.2, 2.5, 3.7], color="darkcyan",
              fill_alpha=0.6, line_color='black', name='vbar4')
    fig4.legend.click_policy = "hide"
    fig4.legend.location = "top_left"
    fig4.legend.background_fill_color = "white"
    fig4.legend.background_fill_alpha = 0.5
    fig4.legend.label_text_color = "#505050"
    fig4.legend.orientation = "vertical"
    fig4.xaxis.axis_label = 'Día de Lectura'
    fig4.add_tools(create_hover(1))
    fig4.yaxis[0].formatter = NumeralTickFormatter(format="0.0a")

    menu6 = Select(title="Error (%):", value='3', name='menu6',
                   options=['1', '2', '3', '4', '5', '6', '7', '8', '9', '10'],
                   css_classes=['mtt_menu6'])

    text2 = Div(text='<b>Criterios de Optimización (w)</b>', css_classes=['mtt_text2'])
    menu7 = Select(title="Clientes:", value='20', name='menu7',
                   options=['0', '10', '20', '30', '40', '50', '60', '70', '80', '90', '100'],
                   css_classes=['mtt_menu7'])
    menu8 = Select(title="Día:", value='40', name='menu8',
                   options=['0', '10', '20', '30', '40', '50', '60', '70', '80', '90', '100'],
                   css_classes=['mtt_menu8'])
    menu9 = Select(title="Dispersión:", value='10', name='menu9',
                   options=['0', '10', '20', '30', '40', '50', '60', '70', '80', '90', '100'],
                   css_classes=['mtt_menu9'])

    widget1 = layout([
        [text2],
        [menu7, menu8, menu9, menu6]
    ])

    checkbox1 = CheckboxGroup(labels=['Simular Paso a Paso'], active=[], name='checkbox1',
                              css_classes=['mtt_checkbox1'])

    button1 = Button(label='Optimizar', button_type="primary",
                     css_classes=['mtt_button1'])
    button1.on_click(controller.optim_days)

    widget2 = layout([
        [checkbox1, button1]
    ])

    text3 = Div(text='Resultados: ', css_classes=['mtt_text3'])

    widget3 = layout([
        [widget1],
        [widget2],
    ])

    widget4 = layout([
        [fig4],
        [widget3, text3]
    ])

    fig5 = figure(plot_width=800, plot_height=300, css_classes=['mtt_fig5'],
                  tools='pan,box_zoom,reset', name='fig5',
                  title='Movimiento de Itinerarios')
    fig5.toolbar.logo = None
    fig5.toolbar_location = 'above'
    fig5.vbar(x=[-3, -2, -1, 0, 1, 2, 3], width=0.5, bottom=0, top=[0, 0, 0, 0, 0, 0, 0],
              color="darkred", fill_alpha=0.6, line_color='black', name='vbar5')
    fig5.legend.click_policy = "hide"
    fig5.legend.location = "top_left"
    fig5.legend.background_fill_color = "white"
    fig5.legend.background_fill_alpha = 0.5
    fig5.legend.label_text_color = "#505050"
    fig5.legend.orientation = "vertical"
    fig5.xaxis.axis_label = 'Días'
    fig5.add_tools(create_hover(1))
    fig5.yaxis[0].formatter = NumeralTickFormatter(format="0.0a")

    # Section 3
    title3 = Div(text='Generación de Agenda', css_classes=['mtt_title3'])

    button2 = Button(label='Ver Impactos', button_type="primary",
                     css_classes=['mtt_button2'])

    text1 = Div(text='<p>Seleccionar Año:</p>', css_classes=['mtt_text1'])

    opts = [str(controller.now.year), str(controller.now.year + 1)]
    rbutton1 = RadioButtonGroup(labels=opts, active=0, name='rbutton1',
                                css_classes=['mtt_rbutton1'])

    button3 = Button(label='Exportar', button_type="success",
                     css_classes=['mtt_button3'])

    # dashboard
    dashboard = layout([
        [title1],
        [menu1, menu2, menu3, menu4, menu5],
        [title2],
        [fig1, fig2],
        [fig3, widget4],
        [fig5],
        [Spacer(height=10)],
        [title3],
        [text1, rbutton1, button2, button3],
    ], sizing_mode='fixed')
    dashboard.name = 'mantenimiento'
    # ini module data
    curdoc().add_root(dashboard)
    menu1.on_change('value', controller.on_change_menus)
    menu2.on_change('value', controller.on_change_menus)
    menu3.on_change('value', controller.on_change_menus)
    menu4.on_change('value', controller.on_change_menus)
    menu5.on_change('value', controller.on_change_menus)
    controller.on_change_menus(None, None, None)


def create_hover(sw):
    if sw == 1:
        hover = HoverTool(
            tooltips="""
                <div>
                    <div>
                        <span style="font-size: 10px; color: #505050;"> @y{0.00a} </span>
                    </div>
                    <div>
                        <span style="font-size: 10px; color: #505050;"> @x </span>
                    </div>
                </div>
            """,
        )
    elif sw == 2:
        hover = HoverTool(
            tooltips="""
                <div>
                    <div>
                        <span style="font-size: 10px; color: #2F2F2F;"> cod_unicom: @cod_unicom </span>
                    </div>
                    <div>
                        <span style="font-size: 10px; color: #2F2F2F;"> ruta: @ruta </span>
                    </div>
                    <div>
                        <span style="font-size: 10px; color: #2F2F2F;"> num_itin: @itin </span>
                    </div>
                </div>
            """,
        )
    return hover
