import dash_core_components as dcc
import dash_html_components as html
import dash_table
import pandas as pd
import numpy as np

from app.helpers import make_graph


def error(msg: str) -> list:
    """
    Creates paragraph with error message.

    Parameters
    ----------
    msg: error message

    Returns
    -------
    A html paragraph:
    [dash_html_components.html.P]
    """
    return [html.P(msg, style={'color': 'red'})]


def button(idx: str, txt: str, align: str = 'right'):
    """
    Creates constant-style button.

    Parameters
    ----------
    idx: button id
    txt: button text
    align: css align parameter

    Returns
    -------
    A html button:
    dash_html_components.html.Button
    """
    return html.Button(txt,
                       id=idx,
                       style={
                           'margin-top': '40px',
                           'float': align,
                           'background-color': '#1EAEDB',
                           'color': 'white'},
                       n_clicks=0)


def graph(cities: list, edges: list):
    """
    Creates plotly network graph using supplied
    cities (nodes) and edges.

    Parameters
    ----------
    cities: list of nodes
    edges: list of edges

    Returns
    -------
    Rendered plotly graph:
    dash_core_components.Graph
    """
    return dcc.Graph(
        id='example-graph',
        figure=make_graph(cities, edges),
        style={
            'width': '100%',
            'height': '1000px',
        }
    )


def upload(idx: str, name: str = 'Select Files'):
    """
    Reusable upload component.
    Parameters
    ----------
    idx: element id
    name: element name

    Returns
    -------
    html div
    """
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


def stats(solve_time: float, solution, cities: list, mean_time: float, input_time: int = 0, new: bool = True):
    """
    Reusable component for solution statistics.

    Parameters
    ----------
    solve_time: time of solving
    solution: Output object
    cities: list of Cities
    input_time: time provided in time.csv
    new: True if for a new solution (requires time.csv)

    Returns
    -------
    html div
    """
    if new:
        worked_time = input_time - solution.time_left
        time_left = solution.time_left
    else:
        worked_time = solution.time_left
        time_left = '?'
    return [
        html.Div([
            html.Li(html.P(f'Solving time: {solve_time:.4f}')),
            html.Li(html.P(f"Path: {', '.join([c.name for c in solution.path])}")),
            html.Li(html.P(f'Time worked: {worked_time}')),
            html.Li(html.P(f'Time left: {time_left}')),
            html.Li(html.P(f'Earned / total: {solution.total}')),
            html.Li(html.P(f'Mean quantity: {float(np.mean([c.value for c in cities])):.2f}')),
            html.Li(html.P(f'Mean time: {mean_time:.2f}')),
            html.A('Download',
                   href="/tmp/solution", target='blank',
                   style={'font-size': '16pt', 'text-transform': 'uppercase'}
                   )
            ])
    ]


def upload_table(name: str, df: pd.DataFrame):
    """
    Reusable component for html table.

    Parameters
    ----------
    name: table name
    df: data frame with data to dispaly

    Returns
    -------
    html div
    """
    df = df.iloc[:20, :]
    return [html.Div([
        html.P(f'File {name} successfully uploaded!'),
        dash_table.DataTable(
            data=df.to_dict('rows'),
            columns=[{'name': i, 'id': i} for i in df.columns],
            style_cell={'textAlign': 'center', 'width': '150px'},
            n_fixed_rows=1,
            style_table={'maxHeight': '300px'},
        ),
    ])]


def vbar():
    """
    Simple horizontal bar.
    """
    return html.Div(style={'height': '3px', 'background-color': '#1EAEDB'})
