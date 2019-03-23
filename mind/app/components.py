import dash_core_components as dcc
import dash_html_components as html
import dash_table

import pandas as pd
import datetime

from app.helpers import make_random_graph


class MainGraph:
    component = dcc.Graph(
            id='example-graph',
            figure=make_random_graph()
        )


class Upload:
    def __init__(self, idx: str, name: str = 'Select Files'):
        self.component = html.Div([
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
### Some nice description and technical info

Dash supports [Markdown](http://commonmark.org/help).

Markdown is a simple way to write and format text.
It includes a syntax for things like **bold text** and *italics*,
[links](http://commonmark.org/help), inline `code` snippets, lists,
quotes, and more.
        ''')


class Vbar:
    component = html.Div(style={'height': '3px', 'background-color': '#1EAEDB'})
