
from bokeh.layouts import layout
from bokeh.models import HoverTool, DatetimeTickFormatter, NumeralTickFormatter, \
    ColumnDataSource, Circle, Range1d, GMapPlot, GMapOptions, PanTool, WheelZoomTool
from bokeh.models.widgets import Select, RadioButtonGroup
from bokeh.plotting import figure, curdoc

from modules.monitoring.controller import Controller

import numpy as np


def create_module(user):
    # start controller
    controller = Controller(user)
    # hover
    hover1 = create_hover(1)
    # module
    fig1 = figure(plot_width=600, plot_height=300,
                  css_classes=['monitoring_fig1'],
                  tools='pan,box_zoom,reset', name='fig1',
                  title='Cantidad de Clientes x día de Lectura')
    fig1.toolbar.logo = None
    fig1.toolbar_location = 'above'
    fig1.vbar(x=[1, 2, 3], width=1000 * 3600 * 24, bottom=0, top=[0, 0, 0],
              color='red', name='vbar2', alpha=0.2)
    line1 = fig1.line(x=[0, 1], y=[0, 1], line_color="darkgray", line_width=2,
                      alpha=0.6, legend='Planificación', name='line1')
    line2 = fig1.line(x=[0, 1], y=[0, 1], line_color="blue", line_width=2,
                      alpha=0.8, legend='Real', name='line1.2')
    fig1.legend.click_policy = "hide"
    fig1.legend.location = "top_left"
    fig1.legend.background_fill_color = "white"
    fig1.legend.background_fill_alpha = 0.5
    fig1.legend.label_text_color = "#505050"
    fig1.legend.orientation = "vertical"
    fig1.xaxis.axis_label = 'Días del mes'
    hover1.renderers = [line1, line2]
    fig1.add_tools(hover1)
    fig1.xaxis.formatter = DatetimeTickFormatter(days=["%d"])
    fig1.yaxis[0].formatter = NumeralTickFormatter(format="0.0a")

    fig2 = figure(plot_width=600, plot_height=300, css_classes=['monitoring_fig2'],
                  tools='pan,box_zoom,reset', name='fig2',
                  title='Cantidad de Itinerarios x día de Lectura')
    fig2.toolbar.logo = None
    fig2.toolbar_location = 'above'
    fig2.vbar(x=[1, 2, 3], width=1000 * 3600 * 24, bottom=0, top=[0, 0, 0],
              color='red', name='vbar3', alpha=0.2)
    line3 = fig2.line(x=[0, 1], y=[0, 1], line_color="darkgray", line_width=2,
                      alpha=0.6, legend='Planificación', name='line2')
    line4 = fig2.line(x=[0, 1], y=[0, 1], line_color="blue", line_width=2,
                      alpha=0.8, legend='Real', name='line2.2')
    fig2.legend.click_policy = "hide"
    fig2.legend.location = "top_left"
    fig2.legend.background_fill_color = "white"
    fig2.legend.background_fill_alpha = 0.5
    fig2.legend.label_text_color = "#505050"
    fig2.legend.orientation = "vertical"
    fig2.xaxis.axis_label = 'Días del mes'
    hover2 = create_hover(1)
    hover2.renderers = [line3, line4]
    fig2.add_tools(hover2)
    fig2.xaxis.formatter = DatetimeTickFormatter(days=["%d"])

    map_options = GMapOptions(lat=10.032663, lng=-74.042470,
                              map_type="roadmap", zoom=7)
    fig3 = GMapPlot(x_range=Range1d(), y_range=Range1d(),
                    map_options=map_options,
                    plot_width=600, plot_height=450, css_classes=['monitoring_fig3'],
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

    menu1 = Select(title="Periodo:", value="opt1", name='menu1',
                   options=["opt1", "opt2", "opt3", "opt4"],
                   width=150, css_classes=['monitoring_menu1'])
    menu1.options = controller.periodos_str
    menu1.value = controller.periodos_str[controller.now.month - 1]

    menu2 = Select(title="Delegación:", value='TODOS', name='menu2',
                   options=['TODOS'],
                   width=200, css_classes=['monitoring_menu2'])

    menu3 = Select(title="Unicom:", value="TODOS", name='menu3',
                   options=["TODOS"],
                   width=150, css_classes=['monitoring_menu3'])

    menu4 = Select(title="Día:", value="TODOS", name='menu4',
                   options=["TODOS"],
                   width=150, css_classes=['monitoring_menu4'])

    menu5 = Select(title="Municipio:", value="TODOS", name='menu5',
                   options=["TODOS"],
                   width=200, css_classes=['monitoring_menu5'])

    menu6 = Select(title="Tipología:", value="TODOS", name='menu6',
                   options=["TODOS"],
                   width=150, css_classes=['monitoring_menu6'])

    fig4 = figure(plot_width=600, plot_height=300, css_classes=['monitoring_fig4'],
                  tools='pan,box_zoom,reset', name='fig4',
                  title='Promedio de Días Facturados')
    fig4.toolbar.logo = None
    fig4.toolbar_location = 'above'
    fig4.line(x=[0, 1], y=[0, 1], line_color="darkgray", line_width=2,
              alpha=0.6, legend='Planificación', name='line4')
    fig4.line(x=[0, 1], y=[0, 1], line_color="blue", line_width=2,
              alpha=0.8, legend='Real', name='line4.2')
    fig4.legend.click_policy = "hide"
    fig4.legend.location = "top_left"
    fig4.legend.background_fill_color = "white"
    fig4.legend.background_fill_alpha = 0.5
    fig4.legend.label_text_color = "#505050"
    fig4.legend.orientation = "vertical"
    fig4.xaxis.axis_label = 'Mes del Año'
    fig4.add_tools(create_hover(4))
    fig4.yaxis[0].formatter = NumeralTickFormatter(format="0.0a")
    # TODO: visualizar el promedio y el total dias facturados al año

    fig5 = figure(plot_width=600, plot_height=300, css_classes=['monitoring_fig5'],
                  tools='pan,box_zoom,reset', name='fig5',
                  title='Histograma de Días Facturados')
    fig5.toolbar.logo = None
    fig5.toolbar_location = 'above'
    fig5.vbar(x=[1, 2, 3], width=0.5, bottom=0, top=[1.2, 2.5, 3.7], color="darkcyan",
              fill_alpha=0.6, line_color='black', name='vbar1', legend='Planificación')
    fig5.line(x=[0, 1], y=[0, 1], line_color="blue", line_width=2,
              alpha=0.8, legend='Real', name='line5.2')
    fig5.legend.click_policy = "hide"
    fig5.legend.location = "top_left"
    fig5.legend.background_fill_color = "white"
    fig5.legend.background_fill_alpha = 0.5
    fig5.legend.label_text_color = "#505050"
    fig5.legend.orientation = "vertical"
    fig5.xaxis.axis_label = 'Días Facturados'
    fig5.add_tools(create_hover(3))
    fig5.yaxis[0].formatter = NumeralTickFormatter(format="0.0a")
    # TODO: agregar curva de suma acumulativa

    fig6 = figure(plot_width=600, plot_height=300, css_classes=['monitoring_fig6'],
                  tools='pan,box_zoom,reset', name='fig6',
                  title='Traslados')
    fig6.toolbar.logo = None
    fig6.toolbar_location = 'above'
    fig6.line(x=[0, 1], y=[0, 1], line_color="darkgray", line_width=2,
              alpha=0.6, legend='Planificación', name='line6')
    fig6.line(x=[0, 1], y=[0, 1], line_color="blue", line_width=2,
              alpha=0.8, legend='Real', name='line6.2')
    fig6.legend.click_policy = "hide"
    fig6.legend.location = "top_left"
    fig6.legend.background_fill_color = "white"
    fig6.legend.background_fill_alpha = 0.5
    fig6.legend.label_text_color = "#505050"
    fig6.legend.orientation = "vertical"
    fig6.xaxis.axis_label = 'Mes del Año'
    fig6.add_tools(create_hover(4))
    fig6.yaxis[0].formatter = NumeralTickFormatter(format="0.0a")

    button_group1 = RadioButtonGroup(
        labels=["Itinerarios", "Energía", "Importe"], active=0,
        name='button_group1',
        css_classes=['monitoring_button_group1'])
    button_group1.on_change('active', controller.on_change_menus)

    widget1 = layout([[fig1], [fig2]], sizing_mode='fixed')
    widget2 = layout([
        [fig3],
        [menu1, menu2, menu3],
        [menu4, menu5, menu6],
    ], sizing_mode='fixed')
    widget3 = layout([[fig6], [button_group1]], sizing_mode='fixed')
    dashboard = layout([
        [widget1, widget2],
        [fig4, fig5],
        [widget3],
    ], sizing_mode='fixed')
    dashboard.name = 'monitoring'
    # ini module data
    curdoc().add_root(dashboard)
    controller.get_user_data()
    controller.populate_menus(controller.info_itin, controller.fechas_itin)
    menu1.on_change('value', controller.on_change_menus)
    menu2.on_change('value', controller.on_change_menus)
    menu3.on_change('value', controller.on_change_menus)
    menu4.on_change('value', controller.on_change_menus)
    menu5.on_change('value', controller.on_change_menus)
    menu6.on_change('value', controller.on_change_menus)
    controller.on_change_menus(None, None, None)


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
    elif sw == 3:
        hover = HoverTool(
            tooltips="""
                <div>
                    <div>
                        <span style="font-size: 10px; color: #505050;"> @x </span>
                    </div>
                    <div>
                        <span style="font-size: 10px; color: #505050;"> @y </span>
                    </div>
                </div>
            """,
        )
    elif sw == 4:
        hover = HoverTool(
            tooltips="""
                <div>
                    <div>
                        <span style="font-size: 10px; color: #505050;"> @x </span>
                    </div>
                    <div>
                        <span style="font-size: 10px; color: #505050;"> @y{0.000a} </span>
                    </div>
                </div>
            """,
        )
    return hover
