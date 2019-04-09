# -*- coding: utf-8 -*-
import time
import dash
import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash_core_components as dcc

from app.components import MainGraph, Upload, Description, Vbar, HoursInput
from app.helpers import parse_contents
from app.solver import tsp

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']


def create_app():
    """
    Dash app factory and layout definition

    Parameters
    ----------

    Returns
    -------

    """
    app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
    app.config['suppress_callback_exceptions'] = True

    app.layout = html.Div([
        html.Div(children=[
            Description.component,
            html.H3('Upload files for tsp solver', style={'margin-top': '40px'}),
            Vbar.component,
            html.Table(children=[
                html.Tr(children=[
                    html.Td(children=[
                        Upload(idx='input-city', name='First upload city-matrix...').component,
                        html.Div(id='output-city')],
                        style={'width': '33%', 'vertical-align': 'top'}),
                    html.Td(children=[
                        Upload(idx='input-coordinates', name='...now we need coordinates...').component,
                        html.Div(id='output-coordinates')],
                        style={'width': '33%', 'vertical-align': 'top'}),
                    html.Td(children=[HoursInput.component], style={'width': '33%', 'vertical-align': 'top'}),
                ])
            ], style={'width': '100%', 'height': '100px'}),
        ]),
        html.Div(children=[
            dcc.Loading([html.Div(id='tsp-graph')], color='#1EAEDB')
        ], style={'margin-top': '40px'})
    ], style={'width': '85%', 'margin-left': '7.5%'})

    # Upload first csv file with time between cities
    @app.callback(Output('output-city', 'children'),
                  [Input('input-city', 'contents')],
                  [State('input-city', 'filename')])
    def upload_city(content, name):
        if content is not None:
            if '.csv' not in name:
                return html.Div(['Only .csv files ar supported!'])
            return html.P(f'File {name} successfully uploaded!')
        return None

    # Upload cities coordinates
    @app.callback(Output('output-coordinates', 'children'),
                  [Input('input-coordinates', 'contents')],
                  [State('input-coordinates', 'filename')])
    def upload_coordinates(content, name):
        if content is not None:
            if '.csv' not in name:
                return html.Div(['Only .csv files ar supported!'])
            return html.P(f'File {name} successfully uploaded!')
        return None

    # Activate solver button if both csv are present
    @app.callback([Output('solve-btn', 'disabled'),
                   Output('solve-btn', 'style')],
                  [Input('input-city', 'contents'),
                   Input('input-coordinates', 'contents')])
    def activate_solver(cities, coords):
        style = {
            'margin-top': '20px',
            'background-color': 'grey',
            'color': 'white'}

        if cities and coords:
            style['background-color'] = '#1EAEDB'
            return False, style
        return True, style

    # Run solver
    @app.callback(Output('tsp-graph', 'children'),
                  [Input('solve-btn', 'n_clicks'),
                   Input('input-city', 'contents'),
                   Input('input-coordinates', 'contents'),
                   Input('hours-number', 'value')])
    def show_graph(n_clicks, city, coords, hours):
        if n_clicks is not None \
                and city is not None \
                and coords is not None \
                and hours is not None \
                and n_clicks > 0:
            # to check loading
            time.sleep(2)

            graph_data = tsp(cities=parse_contents(city),
                             coords=parse_contents(coords),
                             hours=hours)

            return [html.H3(children='The magic TSP graph'), Vbar.component, MainGraph.component]

    return app
