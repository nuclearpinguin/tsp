# -*- coding: utf-8 -*-
import dash
import dash_html_components as html
from dash.dependencies import Input, Output, State

# from app.helpers import parse_contents
from app.components import MainGraph, Upload

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']


def create_app(config):
    app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
    app.config['suppress_callback_exceptions'] = True

    app.layout = html.Div([
        html.Div(children=[
            html.H2('Upload files for TSP solver'),
            html.Table(children=[
                html.Tr(children=[
                    html.Td(children=[
                        Upload(idx='city-matrix', name='Upload city matrix').component,
                        html.Div(id='output-city-matrix')],
                        style={'width': '33%'}),
                    html.Td(children=[
                        html.Div(id='coordinates'),
                        html.Div(id='output-coordinates')],
                        style={'width': '33%'}),
                    html.Td(children=[
                        html.Div(id='info'),
                        html.Div(id='output-info')],
                        style={'width': '33%'})
                ])
            ], style={'width': '100%', 'height': '100px'}),
            html.Button('Solve!', style={'margin-top': '20px', 'visibility': 'hidden'}, id='solve-btn')
        ]),
        html.Div(id='tsp-graph')
    ], style={'width': '90%', 'margin-left': '5%'})

    @app.callback([Output('output-city-matrix', 'children'),
                  Output('coordinates', 'children')],
                  [Input('city-matrix', 'contents')],
                  [State('city-matrix', 'filename'),
                   State('city-matrix', 'last_modified')])
    def upload_city_matrix(content, name, date):
        if content is not None:
            return [html.P('File uploaded 1'),
                    Upload(idx='coordinates-input', name='Upload cities coordinates').component]
        else:
            return [], []

    @app.callback([Output('output-coordinates', 'children'),
                  Output('info', 'children')],
                  [Input('coordinates-input', 'contents')],
                  [State('coordinates-input', 'filename'),
                   State('coordinates-input', 'last_modified')])
    def upload_coordinates(content, name, date):
        if content is not None:
            return [html.P('File uploaded 2'),
                    Upload(idx='info-input', name='Upload additional info').component]
        else:
            return [], []

    @app.callback([Output('output-info', 'children'), Output('solve-btn', 'style')],
                  [Input('info-input', 'contents')],
                  [State('info-input', 'filename'),
                   State('info-input', 'last_modified')])
    def upload_info(content, name, date):
        if content is not None:
            return [html.P('File uploaded 3'), {'margin-top': '20px', 'visibility': 'visible', 'float': 'right'}]
        else:
            return [], []

    @app.callback(Output('tsp-graph', 'children'),
                  [Input('solve-btn', 'n_clicks')])
    def show_graph(n_clicks):
        if n_clicks and n_clicks > 0:
            return [html.H2(children='The magic TSP graph'), MainGraph.component]

    return app
