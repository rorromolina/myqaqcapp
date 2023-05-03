from dash import Dash, dcc, Output, Input, html  # pip install dash
import dash_bootstrap_components as dbc    # pip install dash-bootstrap-components
import plotly.express as px
from conexion import basededatos
from funciones import qaqc, grafico, stats
import pandas as pd
from datetime import datetime as dt
from dash import dash_table

# incorporate data into app
df = basededatos()
lista_assays = df['ASSAYNAME'].unique()
lista_checkstage = df['CHECKSTAGE_CK'].unique()

# Build your components
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# the style arguments for the sidebar. We use position:fixed and a fixed width
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "20rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

# the styles for the main content position it to the right of the sidebar and
# add some padding.
CONTENT_STYLE = {
    "margin-left": "12rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

sidebar = html.Div(
    [
        html.H4("QAQC", className="display-4", style={'fontWeight': 'bold', 'font-size': '28px'}),
        html.Hr(),
        html.P("Seleccione parámetros para personalizar su gráfico", className="lead", style={'fontWeight': 'light', 'font-size': '14px'}),
        html.Label('Seleccione un gráfico:', style={'fontWeight': 'light', 'font-size': '12px'}), 
        dcc.Dropdown(options=['Scatter','RD v Mean Grade', 'ARD v Mean Grade'], value='Scatter', clearable=False, id='charttype', style={'font-size': '12px'}),
        html.Hr(),
        html.Label('Seleccione un análisis:', style={'fontWeight': 'light', 'font-size': '12px'}), 
        dcc.Dropdown(options=lista_assays, value='Au_AA25_ppm', clearable=False, id='assayname', style={'font-size': '12px'}),
        html.Hr(),

        html.Label('Seleccione tipo de control:', style={'fontWeight': 'light', 'font-size': '12px'}), 
        dcc.Dropdown(options=['S','P','C'], value='S', clearable=False, id='checkstage', style={'font-size': '12px'}),
        

        html.Hr(),
        html.Label('Seleccione una fecha:', style={'fontWeight': 'light', 'font-size': '12px'}), 
        dcc.DatePickerRange(id='daterange', start_date=dt(2015, 1, 1),end_date=dt.today(), style={'font-size': '12px'}),

        html.Hr(),
        html.Label('Ingrese los porcentajes para las lineas de control:', style={'fontWeight': 'light', 'font-size': '12px'}), 
        html.Div([
            html.Label('Warning:', style={'fontWeight': 'light', 'margin-right': '10px', 'font-size': '12px'}),
            dcc.Input(id='warningline', type='number', value=10, style={'display': 'inline-block','width': '40px', 'font-size': '12px'}),
            html.Label("Error:", style={'fontWeight': 'light', 'margin-left': '10px', 'font-size': '12px'}),
            dcc.Input(id='errorline', type='number', value=20, style={'display': 'inline-block','width': '40px', 'font-size': '12px', 'margin-left': '10px'})
        ], style={'display': 'inline-block'}), # Agrega 'display: inline-block' aquí
        html.Hr(),
        html.Label('Ancho del grafico:', style={'fontWeight': 'light', 'font-size': '12px'}),
        dcc.Slider(id='ancho', min=500, max=1500, step=50, value=1000, marks={500: '500', 1000: '1000', 1500: '1500'}),
        html.Label('Alto del grafico:', style={'fontWeight': 'light', 'font-size': '12px'}),
        dcc.Slider(id='alto', min=500, max=1000, step=50, value=500, marks={500: '500',750: '750', 1000: '1000'}),
    ],
    style=SIDEBAR_STYLE,
)

mytitle = dcc.Markdown(children='', style={'fontSize': 36}, id='my-title')
mygraph = dcc.Graph(figure={}, id='my-graph')


mytable = dash_table.DataTable(
        id='mydatatable',
        columns=[{"name": 'Muestra Original', "id": 'ID_OR', 'type':'text', 'editable':False},
                 {"name": 'Resultado Orig', "id": 'ASSAYVALUE_OR', 'type':'numeric', 'editable':False},
                 {"name": 'Muestra Duplicada', "id": 'ID_CK', 'type':'text', 'editable':False},
                 {"name": 'Resultado Dup', "id": 'ASSAYVALUE_CK', 'type':'numeric', 'editable':False},        
                 {"name": 'Laboratorio', "id": 'LABCODE_CK', 'type':'text', 'editable':False},
                 {"name": 'Despacho', "id": 'DESPATCHNO_CK', 'type':'text', 'editable':False},
                 {"name": 'LabjobNo', "id": 'LABJOBNO_CK', 'type':'text', 'editable':False},
                 {"name": 'Fecha Retorno', "id": 'FechaACQ', 'type':'datetime', 'editable':False},
                 {"name": 'Status', "id": 'QAQC', 'type':'text', 'editable':False}
                  ],
        data=[],
        filter_action="native",     # allow filtering of data by user ('native') or not ('none')
        sort_action="native",       # enables data to be sorted per-column by user or not ('none')
        sort_mode="single",  # the contents of the table
        style_data_conditional=(
            [
                {'if':{
                    'filter_query': '{QAQC} = "Error"'
                    },
                 'backgroundColor': '#FF4136', 'color': 'white'
                 },
                 {'if':{
                    'filter_query': '{QAQC} = "Advertencia"'
                    },
                 'backgroundColor': '#ffa336', 'color': 'white'
                 },
                 {'if':{
                    'filter_query': '{QAQC} = "Umbral"'
                    },
                 'backgroundColor': '#acf88c', 'color': 'white'
                 }         
                
            ]
        ),
        page_size=8,        
    )

content = html.Div([mytitle, mygraph, mytable], id="page-content", style=CONTENT_STYLE)

# Customize your own Layout
app.layout = dbc.Container([sidebar, content])

# Callback allows components to interact
@app.callback(
    Output('my-title', 'children'),
    Output('my-graph', 'figure'),
    Output('mydatatable', 'data'),
    Input('charttype', 'value'),
    Input('assayname', 'value'),
    Input('daterange', 'start_date'),
    Input('daterange', 'end_date'),
    Input('checkstage', 'value'),
    Input('warningline', 'value'),
    Input('errorline', 'value'),
    Input('ancho', 'value'),
    Input('alto', 'value')	
)
def update_graph(charttype, assayname, dateini, dateend, checkstage, warnignline, errorline, ancho, alto):  # function arguments come from the component property of the Input
    dateini = pd.to_datetime(dateini, format='%Y-%m-%d')
    dateend = pd.to_datetime(dateend, format='%Y-%m-%d')
    # dff = df[(df['ASSAYNAME'] == assayname) & (df['RETURNDATE_CK'] >= dateini) & (df['RETURNDATE_CK'] <= dateend)& (df['CHECKSTAGE_CK'] == checkstage)]
    dff = df.loc[(df['ASSAYNAME'] == assayname) & (df['RETURNDATE_CK'] >= dateini) & (df['RETURNDATE_CK'] <= dateend)& (df['CHECKSTAGE_CK'] == checkstage)]
    dff = dff.assign(QAQC=dff.apply(lambda x: qaqc(x['ASSAYVALUE_OR'], x['ASSAYVALUE_CK'], error=errorline, warning=warnignline), axis=1))
    fig = grafico(dff, charttype, errorline,warnignline, ancho, alto)
    title = 'QAQC Duplicados - ' + assayname
    dff = dff[['ASSAYNAME', 'ID_OR', 'ASSAYVALUE_OR', 'ID_CK', 'ASSAYVALUE_CK', 'RETURNDATE_CK', 'DESPATCHNO_CK', 'LABJOBNO_CK', 'LABCODE_CK','QAQC','FechaACQ']]
    dff = dff.to_dict('records')
    return title, fig, dff  # returned objects are assigned to the component property of the Output


# Run app
if __name__=='__main__':
    app.run(debug=False, port='80')
