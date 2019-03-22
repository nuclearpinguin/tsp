import dash_core_components as dcc
import dash_html_components as html
import dash_table

import pandas as pd
import datetime

class MainGrpah:
    component = html.Div(children=[
        html.H1(children='Hello Dash'),

        html.Div(children='''
                Dash: A web application framework for Python.
            '''),

        dcc.Graph(
            id='example-graph',
            figure={
                'data': [
                    {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'bar', 'name': 'SF'},
                    {'x': [1, 2, 3], 'y': [2, 4, 5], 'type': 'bar', 'name': u'Montréal'},
                ],
                'layout': {
                    'title': 'Dash Data Visualization'
                }
            }
        )
    ])


class Upload:
    component = dcc.Upload(
        id='upload-data',
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
