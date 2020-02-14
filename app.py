# -*- coding: utf-8 -*-
# dash imports
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import pandas as pd
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

import socket
local_ip = [
    l for l in ([
        ip for ip in socket.gethostbyname_ex(socket.gethostname())[2]
        if not ip.startswith("127.")][:1],
        [[(s.connect(('8.8.8.8', 53)), s.getsockname()[0], s.close())
          for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]])
    if l][0][0]


def make_layout():
    df_table = pd.read_csv('data/bme280.csv', index_col=0)
    labels = [label for label in df_table.columns if label != "Zeit"]

    return html.Div(
        children=[
            html.H1(children='Wetterdaten'),

            html.Div(children='Dash: A web application framework for Python.'),
            html.Div('Aus dieser Tabelle kannst du die Messerwerte des BME '
                     'Sensors entnehmen.', id='description'),
            # html.Div(children=[
            #     html.Div('Number one'),
            #     html.Div('Number two')], className='horizontal'),
            dcc.Interval(id='update-table', interval=10000),
            dash_table.DataTable(
                id='table',
                columns=[{"name": i, "id": i} for i in df_table.columns],
                data=df_table.to_dict('records'),
                style_table={
                    'maxHeight': '300px',
                    'overflowY': 'scroll'
                },
                filter_action="native",
                sort_action="native",
                fixed_rows={'headers': True, 'data': 0}
            ),
            dcc.Dropdown(
                id='data-select',
                options=[
                    {'label': i, 'value': i}
                    for i in labels
                ],
                multi=False),
            dcc.Graph(
                id='example-graph',
                figure={
                    'data': [
                    ],
                    'layout': {
                        'title': 'Dash Data Visualization'
                    }
                }
            )
        ]
    )


demo_app = dash.Dash(__name__)
demo_app.layout = make_layout()


@demo_app.callback(
    Output('table', 'data'),
    [Input('update-table', 'n_intervals')])
def update_data(n):
    df = pd.read_csv('data/bme280.csv', index_col=0)
    return df.to_dict('records')


# @demo_app.callback(
#     Output(component_id='example-graph', component_property='figure'),
#     [Input(component_id='data-select', component_property='value')],
#     [State(component_id='example-graph', component_property='figure')])
# def update_country(properties, fig):
#     if properties is None:
#         raise PreventUpdate
#
#     df = pd.read_csv('data/bme280.csv', index_col=0)
#
#     fig = {
#         'data': [
#             extract_data(property, df)
#             for property in properties
#         ],
#         'layout': {
#             'title': 'Dash Data Visualization'
#         }
#     }
#
#     return fig


@demo_app.callback(
    Output(component_id='example-graph', component_property='figure'),
    [Input(component_id='data-select', component_property='value')],
    [State(component_id='example-graph', component_property='figure')])
def update_data(property, fig):
    if property is not None:
        df = pd.read_csv('data/bme280.csv', index_col=0)
        fig = {
            'data': [
                extract_data(property, df)
            ],
            'layout': {
                'title': 'Dash Data Visualization'
            }
        }

    return fig


def extract_data(property, df):
    print(property)
    return {
        'x': df["Zeit"],
        'y': df[property],
        'mode': 'lines',
        'name': property
    }

if __name__ == '__main__':
    demo_app.run_server(debug=True, host=local_ip)
