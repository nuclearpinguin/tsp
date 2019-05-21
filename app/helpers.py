import base64
import io
import plotly.graph_objs as go
import networkx as nx
import pandas as pd
from plotly.graph_objs.scatter import Marker
from typing import List
from functools import reduce
from time import time as now

from app.solvers import City


def prepare_data(cities: List[City]) -> list:
    return [(city.name, {'pos': (city.x, city.y), 'name': city.name, 'quantity': city.value})
            for city in cities]


def parse_contents(contents: str, columns=None) -> pd.DataFrame:
    """
    Helper for parsing uploaded .csv file
    """
    if not contents:
        return pd.DataFrame([])

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


def make_graph(nodes: list, edges: list):
    G = nx.Graph()

    # Create graph
    G.add_nodes_from(nodes)
    G.add_edges_from(edges)

    # Hack
    edge_labels_x = []
    edge_labels_y = []
    edge_labels_txt = []

    # Define appends for better performance
    add_x = edge_labels_x.append
    add_y = edge_labels_y.append
    add_txt = edge_labels_txt.append

    tic = now()

    # Create edges plot
    edge_traces = []
    add = edge_traces.append
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
        add(trace)
        add_x((x0 + x1) / 2)
        add_y((y0 + y1) / 2)
        add_txt(f"time: {info['time'] }")

    print(f'edges : {now() - tic}')

    # Hack for info hover on edges:
    middle_node_trace = go.Scatter(
        x=edge_labels_x,
        y=edge_labels_y,
        text=edge_labels_txt,
        mode='markers',
        hoverinfo='text',
        marker=Marker(opacity=0)
    )

    node_trace = go.Scatter(
        x=[],
        y=[],
        text=[],
        mode='markers',
        hoverinfo='text',
        marker=Marker(
            color=[],
            size=10,
            line=dict(width=2))
    )

    tic = now()

    # Create nodes plot
    for node in G.nodes():
        the_node = G.node[node]
        x, y = the_node['pos']
        node_trace['x'] += tuple([x])
        node_trace['y'] += tuple([y])
        node_info = reduce(lambda a, b: f'{a} | {b}', [f'{k} : {v}' for k, v in the_node.items()])
        node_trace['text'] += tuple([node_info])

    print(f'edges : {now() - tic}')

    data = edge_traces + [node_trace, middle_node_trace]

    return go.Figure(data=data,
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
                         yaxis=dict(showgrid=False, zeroline=False, showticklabels=False,
                                    scaleanchor="x", scaleratio=1),
                     ))
