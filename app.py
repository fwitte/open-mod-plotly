# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import pandas as pd
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate


def extract_country(country_iso, df):
    return {
        'x': df.loc[country_iso].year,
        'y': df.loc[country_iso].fertility,
        'mode': 'lines+markers',
        'name': df.loc[country_iso].country.unique()[0]
    }

df_table = pd.read_csv('data/children-per-woman-UN.csv')
df = df_table.set_index('country_iso')

# loading external resources
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
options = dict(
    # external_stylesheets=external_stylesheets
)

demo_app = dash.Dash(__name__, **options)

demo_app.layout = html.Div(
    children=[
        html.H1(children='Hello openmod'),

        html.Div(children='Dash: A web application framework for Python.'),
        html.Div('Here is a div', id='someuniquestuff'),
        # html.Div(children=[
        #     html.Div('Number one'),
        #     html.Div('Number two')], className='horizontal'),
        # dash_table.DataTable(
        #     id='table',
        #     columns=[{"name": i, "id": i} for i in df_table.columns],
        #     data=df_table.to_dict('records'),
        #     style_table={
        #         'maxHeight': '300px',
        #         'overflowY': 'scroll'
        #     },
        #     filter_action="native",
        #     sort_action="native",
        #     fixed_rows={'headers': True, 'data': 0}
        # ),
        dcc.Dropdown(
            id='country-select',
            options=[
                {'label': df.loc[i].country.unique()[0], 'value': i}
                for i in df_table.country_iso.dropna().unique()
            ],
            multi=True),
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

# @demo_app.callback(
#     Output(component_id='example-graph', component_property='figure'),
#     [Input(component_id='country-select', component_property='value')],
#     [State(component_id='example-graph', component_property='figure')])
# def update_country(country_iso, fig):
#     if country_iso is not None:
#         fig = {
#             'data': [
#                 extract_country(country_iso, df)
#             ],
#             'layout': {
#                 'title': 'Dash Data Visualization'
#             }
#         }

#     return fig

@demo_app.callback(
    [Output(component_id='example-graph', component_property='figure'),
     Output(component_id='someuniquestuff', component_property='children')],
    [Input(component_id='country-select', component_property='value')],
    [State(component_id='example-graph', component_property='figure')])
def update_country(countries, fig):
    if countries is None:
        raise PreventUpdate

    fig = {
        'data': [
            extract_country(country_iso, df)
            for country_iso in countries
        ],
        'layout': {
            'title': 'Dash Data Visualization'
        }
    }

    return fig, countries

if __name__ == '__main__':
    demo_app.run_server(debug=True, host='192.168.178.23')
