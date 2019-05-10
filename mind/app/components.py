import dash_core_components as dcc
import dash_html_components as html
import dash_table

import pandas as pd
import datetime

from app.helpers import make_graph


def graph(cities, edges):
    return dcc.Graph(
        id='example-graph',
        figure=make_graph(cities, edges),
        style={
            'width': '100%',
            'height': '1000px',
        }
    )


def upload(idx: str, name: str = 'Select Files'):
    return html.Div([
        html.P(name),
        dcc.Upload(
            id=idx,
            contents=None,
            filename=None,
            children=html.Div([
                'Drag and Drop or ',
                html.A('Select Files')
            ]),
            style={
                'width': '100%',
                'height': '60px',
                'lineHeight': '60px',
                'borderWidth': '1px',
                'borderStyle': 'dashed',
                'borderRadius': '5px',
                'textAlign': 'center',
                'margin': '10px'
            },
        )
    ])


def upload_table(contents: str, filename: str, time_stamp: int, df: pd.DataFrame):
    return html.Div([
        html.H5(filename),
        html.H6(datetime.datetime.fromtimestamp(time_stamp)),

        dash_table.DataTable(
            data=df.to_dict('rows'),
            columns=[{'name': i, 'id': i} for i in df.columns]
        ),

        html.Hr(),  # horizontal line

        # For debugging, display the raw contents provided by the web browser
        html.Div('Raw Content'),
        html.Pre(contents[0:200] + '...', style={
            'whiteSpace': 'pre-wrap',
            'wordBreak': 'break-all'
        })
    ])


def description():
    return dcc.Markdown('''
### About the Traveling Salesman Problem

Given a list of cities and the distances between each pair of cities, 
what is the shortest possible route that visits each city and returns to the origin city? 
([Wiki](http://commonmark.org/help))

This app allows you to solve the problem. But first you have to upload three files:

- Matrix of connections between cities

- Cities coordinates

- Additional information about each city
        ''')


def vbar():
    return html.Div(style={'height': '3px', 'background-color': '#1EAEDB'})
