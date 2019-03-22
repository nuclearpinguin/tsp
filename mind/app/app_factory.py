# -*- coding: utf-8 -*-
import dash
import dash_html_components as html
from dash.dependencies import Input, Output, State

from app.helpers import parse_contents
from app.components import MainGrpah, Upload

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']


def create_app(config):
    app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

    app.layout = html.Div([
        MainGrpah.component,
        Upload.component,
        html.Div(id='output-data-upload')
    ])

    @app.callback(Output('output-data-upload', 'children'),
                  [Input('upload-data', 'contents')],
                  [State('upload-data', 'filename'),
                   State('upload-data', 'last_modified')])
    def update_output(content, name, date):
        if content is not None:
            children = [parse_contents(content, name, date)]
            return children

    return app
