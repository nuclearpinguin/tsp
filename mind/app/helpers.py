import base64
import io
import plotly.graph_objs as go
from plotly.graph_objs.scatter import Marker
import networkx as nx
from typing import List, Tuple
import pandas as pd
from functools import reduce
from random import randint

from .solver import City


def prepare_data(cities: pd.DataFrame, paths: pd.DataFrame, time: pd.DataFrame):
    cities = [City(name, x, y, q) for name, x, y, q in cities.values]
    edges = [(from_c, to_c, {'time': t, 'solution': randint(0, 1)}) for from_c, to_c, t in paths.values]
    return cities, edges


def parse_contents(contents: str) -> pd.DataFrame:
    """
    Helper for parsing uploaded .csv file

    Parameters
    ----------
    contents

    Returns
    -------

    """
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    try:
        # Assume that the user uploaded a CSV file
        df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
        return df
    except Exception as e:
        print(e)
        return pd.DataFrame([])


def _color_edge(info: dict) -> dict:
    if info['solution']:
        return dict(width=8, color='#1EAEDB')
    return dict(width=0.8, color='#888')


def make_graph(cities: List[City], edges: List[Tuple[str, str]]):
    G = nx.Graph()

    nodes = [(city.name, {'pos': (city.x, city.y), 'name': city.name, 'quantity': city.value}) for city in cities]

    # Create graph
    G.add_nodes_from(nodes)
    G.add_edges_from(edges)

    # Hack for info hover on edges:
    middle_node_trace = go.Scatter(
        x=[],
        y=[],
        text=[],
        mode='markers',
        hoverinfo='text',
        marker=Marker(opacity=0)
    )

    # Create edges plot
    edge_traces = []
    for edge in G.edges(data=True):
        a, b, info = edge
        x0, y0 = G.node[a]['pos']
        x1, y1 = G.node[b]['pos']
        trace = go.Scatter(
            x=[x0, x1, None],
            y=[y0, y1, None],
            line=_color_edge(info),
            hoverinfo='none',
            mode='lines'
        )
        edge_traces.append(trace)

        # Create magic hover info on edge
        middle_node_trace['x'] += tuple([(x0 + x1) / 2])
        middle_node_trace['y'] += tuple([(y0 + y1) / 2])
        middle_node_trace['text'] += tuple([f"time: {info['time'] }"])

    node_trace = go.Scatter(
        x=[],
        y=[],
        text=[],
        mode='markers',
        hoverinfo='text',
        marker=dict(
            color=[],
            size=10,
            line=dict(width=2)))

    # Create nodes plot
    for node in G.nodes():
        x, y = G.node[node]['pos']
        node_trace['x'] += tuple([x])
        node_trace['y'] += tuple([y])
        node_info = reduce(lambda a, b: f'{a} | {b}', [f'{k} : {v}' for k, v in G.node[node].items()])
        node_trace['text'] += tuple([node_info])

    return go.Figure(data=[*edge_traces, node_trace, middle_node_trace],
                     layout=go.Layout(
                         showlegend=False,
                         hovermode='closest',
                         margin=dict(b=20, l=5, r=5, t=40),
                         annotations=[dict(
                             text='',
                             showarrow=False,
                             xref="paper", yref="paper",
                             x=0.005, y=-0.002)],
                         xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                         yaxis=dict(showgrid=False, zeroline=False, showticklabels=False, scaleanchor="x", scaleratio=1),
                     ))
