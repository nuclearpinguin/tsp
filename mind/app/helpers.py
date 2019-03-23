import base64
import io
import plotly.graph_objs as go
import networkx as nx

import pandas as pd
from functools import reduce


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


def make_graph():
    G = nx.Graph()

    nodes = [
        (0, {'pos': (1, 0), 'name': 'Node 0'}),
        (1, {'pos': (2, 0), 'name': 'Node 1'}),
        (2, {'pos': (3, 0), 'name': 'Node 2'}),
        (3, {'pos': (4, 0), 'name': 'Node 3'}),
    ]

    edges = [(1, 2)]

    # Create graph
    G.add_nodes_from(nodes)
    G.add_edges_from(edges)


    # Creates scatter plot
    edge_trace = go.Scatter(
        x=[],
        y=[],
        line=dict(width=0.8, color='#888'),
        hoverinfo='none',
        mode='lines')

    # Unpack nodes positions and make scatter
    for edge in G.edges():
        x0, y0 = G.node[edge[0]]['pos']
        x1, y1 = G.node[edge[1]]['pos']
        edge_trace['x'] += tuple([x0, x1, None])
        edge_trace['y'] += tuple([y0, y1, None])

    node_trace = go.Scatter(
        x=[],
        y=[],
        text=[],
        mode='markers',
        hoverinfo='text',
        marker=dict(
            color=[],
            size=10,
            # colorbar=dict(
            #     thickness=15,
            #     title='Node Connections',
            #     xanchor='left',
            #     titleside='right'
            # ),
            line=dict(width=2)))

    # Add nodes attributes
    for node in G.nodes():
        x, y = G.node[node]['pos']
        node_trace['x'] += tuple([x])
        node_trace['y'] += tuple([y])
        node_info = reduce(lambda a, b: f'{a} | {b}', [f'{k} : {v}' for k, v in G.node[node].items()])
        node_trace['text'] += tuple([node_info])

    return go.Figure(data=[edge_trace, node_trace],
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
                         yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)))
