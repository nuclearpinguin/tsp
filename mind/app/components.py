import dash_core_components as dcc
import dash_html_components as html
import dash_table

import pandas as pd
import datetime

from app.helpers import make_graph


class MainGraph:
    component = dcc.Graph(
            id='example-graph',
            figure=make_graph()
        )


class Upload:
    def __init__(self, idx: str, name: str = 'Select Files'):
        self.component = html.Div([
            html.P(name),
            dcc.Upload(
                id=idx,
                contents=None,
                multiple=False,
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


class HoursInput:
    component = html.Div([
            html.P("... and finally the number of working hours"),
            dcc.Input(id='hours-number', type='text', value='12'),
            html.Button('Solve!',
                        id='solve-btn',
                        n_clicks=0,
                        disabled=True,
                        style={
                            'margin-top': '20px',
                            'background-color': 'grey',
                            'color': 'white'}),
            ])


class UploadedTable:
    def __init__(self, contents: str, filename: str, time_stamp: int, df: pd.DataFrame):
        self.component = html.Div([
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


class Description:
    component = dcc.Markdown('''
### About the Traveling Salesman Problem

Given a list of cities and the distances between each pair of cities, 
what is the shortest possible route that visits each city and returns to the origin city? 
([Wiki](http://commonmark.org/help))

This app allows you to solve the problem. But first you have to upload three files:

- Matrix of connections between cities

- Cities coordinates

- Additional information about each city
        ''')


class Vbar:
    component = html.Div(style={'height': '3px', 'background-color': '#1EAEDB'})
