# -*- coding: utf-8 -*-
import time

import dash
import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash_core_components as dcc

# from app.helpers import parse_contents
from app.components import MainGraph, Upload, Description, Vbar
from app.helpers import parse_contents
from app.solver import tsp

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']


def create_app(config):
    """
    Dash app factory and layout definition

    Parameters
    ----------
    config

    Returns
    -------

    """
    app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
    app.config['suppress_callback_exceptions'] = True

    app.layout = html.Div([
        html.Div(children=[
            Description.component,
            html.H3('Upload files for tsp solver'),
            Vbar.component,
            html.Table(children=[
                html.Tr(children=[
                    html.Td(children=[
                        Upload(idx='city-matrix-input', name='Upload city matrix').component,
                        html.Div(id='output-city-matrix')],
                        style={'width': '33%', 'vertical-align': 'top'}),
                    html.Td(children=[
                        html.Div(id='coordinates-input'),
                        html.Div(id='output-coordinates')],
                        style={'width': '33%', 'vertical-align': 'top'}),
                    html.Td(children=[
                        html.Div(id='info-input'),
                        html.Div(id='output-info')],
                        style={'width': '33%', 'vertical-align': 'top'}),
                ])
            ], style={'width': '100%', 'height': '100px'}),
            html.Button('Solve!', id='solve-btn', style={'display': 'none'}, n_clicks=0),
        ]),
        html.Div(children=[
            dcc.Loading([html.Div(id='tsp-graph')], color='#1EAEDB')
        ], style={'margin-top': '40px'})
    ], style={'width': '85%', 'margin-left': '7.5%'})

    @app.callback([Output('output-city-matrix', 'children'),
                  Output('coordinates-input', 'children')],
                  [Input('city-matrix-input', 'contents')],
                  [State('city-matrix-input', 'filename')])
    def upload_city_matrix(content, name):
        if content is not None:
            if '.csv' not in name:
                return [html.Div(['Only .csv files ar supported!']), []]

            return [html.P(f'File {name} successfully uploaded!'),
                    Upload(idx='coordinates-input', name='Upload cities coordinates').component]
        return None, None

    @app.callback([Output('output-coordinates', 'children'),
                  Output('info-input', 'children')],
                  [Input('coordinates-input', 'contents')],
                  [State('coordinates-input', 'filename')])
    def upload_coordinates(content, name):
        if content is not None:
            if '.csv' not in name:
                return [html.Div(['Only .csv files ar supported!']), []]

            return [html.P(f'File {name} successfully uploaded!'),
                    Upload(idx='info-input', name='Upload additional info').component]
        return None, None

    @app.callback([Output('output-info', 'children'),
                   Output('solve-btn', 'style')],
                  [Input('info-input', 'contents')],
                  [State('info-input', 'filename')])
    def upload_info(content, name):
        if content is not None:
            if '.csv' not in name:
                return [html.Div(['Only .csv files ar supported!']), {'visibility': 'hidden'}]

            return [html.P(f'File {name} successfully uploaded!'),
                    {'margin-top': '20px', 'visibility': 'visible',
                     'float': 'right', 'background-color': '#1EAEDB', 'color': 'white'}]

        return None, {'visibility': 'hidden'}

    @app.callback(Output('tsp-graph', 'children'),
                  [Input('solve-btn', 'n_clicks'),
                   Input('city-matrix-input', 'contents'),
                   Input('coordinates-input', 'contents'),
                   Input('info-input', 'contents')])
    def show_graph(n_clicks, city, coords, info):
        if n_clicks is not None \
                and city is not None \
                and coords is not None \
                and info is not None \
                and n_clicks > 0:
            # to check loading
            time.sleep(2)

            graph_data = tsp(cities=parse_contents(city),
                             coords=parse_contents(coords),
                             info=parse_contents(info))

            return [html.H3(children='The magic TSP graph'), Vbar.component, MainGraph.component]

    return app
