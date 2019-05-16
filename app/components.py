import dash_core_components as dcc
import dash_html_components as html
import dash_table
import pandas as pd
import numpy as np

from app.helpers import make_graph


def error(msg: str):
    return html.P(msg, style={'color': 'red'})


def button(idx: str, txt: str, align: str = 'right'):
    return html.Button(txt,
                       id=idx,
                       style={
                           'margin-top': '40px',
                           'float': align,
                           'background-color': '#1EAEDB',
                           'color': 'white'},
                       n_clicks=0)


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


def stats(solve_time: float, solution, cities):
    return [
        html.Div([
            html.H6('SOLUTION:'),
            html.Li(html.P(f'Solving time: {solve_time:.4f}')),
            html.Li(html.P(f"Path: {', '.join([c.name for c in solution.path])}")),
            html.Li(html.P(f'Time left: {solution.time_left}')),
            html.Li(html.P(f'Earned / total: {solution.total}')),
            html.Li(html.P(f'Mean quantity: {float(np.mean([c.value for c in cities])):.2f}')),
            html.A('Download', href="/tmp/solution", target='blank')
            ])
    ]


def upload_table(name: str, df: pd.DataFrame):
    df = df.iloc[:20, :]
    return html.Div([
        html.P(f'File {name} successfully uploaded!'),
        dash_table.DataTable(
            data=df.to_dict('rows'),
            columns=[{'name': i, 'id': i} for i in df.columns],
            style_cell={'textAlign': 'center', 'width': '150px'},
            n_fixed_rows=1,
            style_table={'maxHeight': '300px'},
        ),
    ])


def vbar():
    return html.Div(style={'height': '3px', 'background-color': '#1EAEDB'})
