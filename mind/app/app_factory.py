# -*- coding: utf-8 -*-
import time
import numpy as np
import dash
import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import pandas as pd
import dash_table

from app.components import graph, vbar, upload, upload_table, stats, button
from app.helpers import parse_contents, prepare_data
from app.solver import make_plot_data

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']


def create_app():
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
        dcc.Store(id='memory'),
        html.Div(children=[
            html.H3('Files upload', style={'margin-top': '40px'}),
            vbar(),
            html.Table(children=[
                html.Tr(children=[
                    html.Td(
                        id='city-upload',
                        children=[
                        upload(idx='city-matrix-input', name='First upload city-matrix...'),
                        html.Div(id='output-city-matrix')],
                        style={'width': '33%', 'vertical-align': 'top'}),

                    html.Td(children=[
                        upload(idx='coordinates-input', name='...now we need coordinates...'),
                        html.Div(id='output-coordinates')],
                        style={'width': '33%', 'vertical-align': 'top'}),

                    html.Td(children=[
                        upload(idx='info-input', name='...finally add some info'),
                        html.Div(id='output-info')],
                        style={'width': '33%', 'vertical-align': 'top'}),
                ])
            ], style={'width': '100%', 'height': '100px'}),
            button('solve-btn', 'solve'),
        ]),

        html.Div(children=[
            html.Div(id='save-prompt', children=[]),
            dcc.Loading([html.Div(id='tsp-solution', children=[])], color='#1EAEDB'),
            dcc.Loading([html.Div(id='tsp-graph', children=[])], color='#1EAEDB')
        ], style={'margin-top': '40px'})

    ], style={'width': '85%', 'margin-left': '7.5%'})

    @app.callback([Output('output-city-matrix', 'children')],
                  [Input('city-matrix-input', 'contents')],
                  [State('city-matrix-input', 'filename')])
    def upload_city_matrix(content, name):
        if content is not None:
            # TODO: validate input
            if '.csv' not in name:
                return html.Div(['Only .csv files ar supported!']),
            df = parse_contents(content)
            return upload_table(name, df),
        return None,

    @app.callback([Output('output-coordinates', 'children')],
                  [Input('coordinates-input', 'contents')],
                  [State('coordinates-input', 'filename')])
    def upload_coordinates(content, name):
        if content is not None:
            if '.csv' not in name:
                return html.Div(['Only .csv files ar supported!']),
            df = parse_contents(content)
            return upload_table(name, df),
        return None,

    @app.callback([Output('output-info', 'children')],
                  [Input('info-input', 'contents')],
                  [State('info-input', 'filename')])
    def upload_info(content, name):
        if content is not None:
            if '.csv' not in name:
                return [html.Div(['Only .csv files ar supported!']), {'visibility': 'hidden'}]
            df = parse_contents(content)
            return upload_table(name, df),
        return None,

    @app.callback([Output('tsp-solution', 'children'), Output('memory', 'data')],
                  [Input('solve-btn', 'n_clicks'),
                   Input('city-matrix-input', 'contents'),
                   Input('coordinates-input', 'contents'),
                   Input('info-input', 'contents')],
                  [State('memory', 'data')])
    def generate_solution(n_clicks, city, coords, df_time, cache):
        if n_clicks and city and coords and df_time and n_clicks > 0:
            tic = time.time()

            solution, cities, edges = make_plot_data(cities=parse_contents(city),
                                                     paths=parse_contents(coords),
                                                     time=parse_contents(df_time))

            solving_time = time.time() - tic

            output = [html.H3(children='The magic TSP graph'), vbar()]
            output += stats(solving_time, 1200, solution, cities)

            # tic = time.time()
            # plot = graph(cities, edges)
            # plotting_time = time.time() - tic
            # output += [plot]
            cache = {'cities': prepare_data(cities), 'edges': list(edges)}
            return output, cache

        if n_clicks is not None and n_clicks > 0:
            return [html.P('no data')], dict()

        return None, dict()

    @app.callback([Output('tsp-graph', 'children')],
                  [Input('memory', 'data')],
                  [State('memory', 'data')])
    def show_plot(n_clicks, cache):
        if cache:
            cities, edges = cache.values()
            tic = time.time()
            plot = graph(cities, edges)
            plotting_time = time.time() - tic
            return plot,
        return None,


    @app.callback([Output('save-prompt', 'children')],
                  [Input('save-btn', 'n_clicks')])
    def save_solution(n_clicks):
        if n_clicks and n_clicks > 0:
            print('saved')
            return [html.P('works')]

        return None,
    return app
