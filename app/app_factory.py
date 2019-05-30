# -*- coding: utf-8 -*-
import time
import dash
import flask
import dash_daq as daq
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State


import app.components as comp
import app.file_handlers as fh
from app.helpers import parse_contents, prepare_data
from app.solvers import make_plot_data, data_from_solution


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

CLICKS = 0


def create_app():
    """
    Dash app factory and layout definition.
    """
    app = dash.Dash(__name__, external_stylesheets=external_stylesheets, sharing=True)
    app.config['suppress_callback_exceptions'] = True

    app.layout = html.Div([
        dcc.Store(id='memory'),
        dcc.Store(id='params'),
        html.Div(children=[
            html.H3(id='problem-type', style={'margin-top': '40px', 'display': 'inline-block'}),
            daq.BooleanSwitch(
                id='type-switch',
                on=False,
                style={'margin-left': '20px', 'display': 'inline-block'}
            ),
            comp.vbar(),
            html.Table(children=[
                html.Tr(id='upload-row', children=[
                    html.Td(children=[
                        comp.upload(idx='city-input', name='City coordinates:'),
                        html.Div(id='output-city')],
                        style={'width': '33%', 'vertical-align': 'top'}),

                    html.Td(children=[
                        comp.upload(idx='paths-input', name='Paths information'),
                        html.Div(id='paths-output')],
                        style={'width': '33%', 'vertical-align': 'top'}),

                    html.Td(children=[
                        comp.upload(idx='time-solution-input', name='Magic .csv with time:'),
                        html.Div(id='time-output')],
                        style={'width': '33%', 'vertical-align': 'top'}),
                ]),
            ], style={'width': '100%', 'height': '100px'}),
            daq.BooleanSwitch(
                id='exact-solver',
                on=False,
                label='Use exact solver',
                labelPosition='top',
                style={'margin-right': '20px', 'display': 'inline-block'}
            ),
            daq.BooleanSwitch(
                id='plot-switch',
                on=True,
                label='Plot solution',
                labelPosition='top',
                style={'margin-right': '20px', 'display': 'inline-block'}
            ),
            html.Div(id='time-slider-output', style={'margin-top': '10px'}),
            dcc.Slider(min=5, max=65, value=15, id='time-slider',
                       marks={(5 * (i+1)): f'{5 * (i+1)}s' for i in range(13)}),

            html.Div(id='simulations-slider-output', style={'margin-top': '40px'}),
            dcc.Slider(min=10, max=490, value=90, id='simulations-slider',
                       marks={(10 * i * i): f'{10 * i * i}' for i in range(1, 10)}),
            comp.button('solve-btn', 'solve'),
        ]),

        html.Div(children=[
            dcc.Loading([html.Div(id='tsp-solution')], color='#1EAEDB'),
            dcc.Loading([html.Div(id='tsp-graph')], color='#1EAEDB')
        ], style={'margin-top': '40px'})

    ], style={'width': '85%', 'margin-left': '7.5%'})

    @app.callback([Output('output-city', 'children')],
                  [Input('city-input', 'contents')],
                  [State('city-input', 'filename')])
    def upload_city_matrix(content, name):
        if content:
            if '.csv' not in name:
                return html.Div(comp.error('Only .csv files ar supported!')),

            df = parse_contents(content)
            result = fh.validate_cities(df)
            if not result.status:
                return comp.error(result.msg)

            return comp.upload_table(name, df)
        return [None]

    @app.callback([Output('paths-output', 'children')],
                  [Input('paths-input', 'contents'), Input('city-input', 'contents')],
                  [State('paths-input', 'filename')])
    def upload_paths(content, cities, name):
        if content:
            if '.csv' not in name:
                return html.Div(comp.error('Only .csv files ar supported!')),

            df = parse_contents(content)
            cities = parse_contents(cities)
            result = fh.validate_paths(df, cities)
            if not result.status:
                return comp.error(result.msg)

            return comp.upload_table(name, df)
        return [None]

    @app.callback([Output('time-output', 'children')],
                  [Input('type-switch', 'on'), Input('time-solution-input', 'contents')],
                  [State('time-solution-input', 'filename')])
    def upload_time_solution(old_solution, content, name):
        if old_solution and content:
            if '.txt' not in name:
                return html.Div(comp.error('Only .txt files ar supported!')),

            result = fh.validate_solution(content)
            if not result.status:
                return comp.error(result.msg)
            return [html.Div([html.P(f'File {name} successfully uploaded!')])]

        if content:
            if '.csv' not in name:
                return [html.Div(comp.error('Only .csv files ar supported!'))]

            df = parse_contents(content)
            result = fh.validate_time(df)
            if not result.status:
                return comp.error(result.msg)

            return comp.upload_table(name, df)
        return [None]

    @app.callback([Output('tsp-solution', 'children'), Output('memory', 'data')],
                  [Input('type-switch', 'on'),
                   Input('exact-solver', 'on'),
                   Input('solve-btn', 'n_clicks'),
                   Input('city-input', 'contents'),
                   Input('paths-input', 'contents'),
                   Input('time-solution-input', 'contents'),
                   Input('simulations-slider', 'value'),
                   Input('time-slider', 'value')
                   ],
                  [State('memory', 'data')])
    def generate_solution(old_solution, exact, n_clicks, city, paths, df_time, n_sim, time_limit, cache):
        global CLICKS
        if old_solution and n_clicks and n_clicks > CLICKS:
            solution_content = df_time
            if solution_content:
                CLICKS += 1
                solution = fh.solution_to_output(solution_content)

                if city and paths:
                    mean_time = paths.travel_time.mean()
                    cities, edges = data_from_solution(cities=parse_contents(city),
                                                       paths=parse_contents(paths),
                                                       solution=solution)
                else:
                    mean_time = None
                    cities, edges = data_from_solution(cities=None,
                                                       paths=None,
                                                       solution=solution)

                # Save solution
                fh.save_solution(solution, solution.time_left, new=False)

                # Generate html elements
                output = [html.H3(children='Solution'), comp.vbar()]
                output += comp.stats(0.0, solution, cities, new=False, mean_time=mean_time)

                # Cache data
                cache = {'cities': prepare_data(cities), 'edges': list(edges)}

                return output, cache

        # New solution
        elif n_clicks and city and paths and df_time and n_clicks > CLICKS:
            CLICKS += 1

            tic = time.time()
            df_time = parse_contents(df_time)
            mean_time = paths.travel_time.mean()
            solution, cities, edges = make_plot_data(cities=parse_contents(city),
                                                     paths=parse_contents(paths),
                                                     time=df_time,
                                                     simulations=n_sim,
                                                     time_limit=time_limit,
                                                     exact=exact)
            solving_time = time.time() - tic

            # Save solution
            fh.save_solution(solution, df_time.time.values[0])

            # Generate html elements
            output = [html.H3(children='Solution'), comp.vbar()]
            output += comp.stats(solving_time, solution, cities, df_time.time.values[0], mean_time=mean_time)

            # Cache data
            cache = {'cities': prepare_data(cities), 'edges': list(edges)}

            return output, cache

        return [None], None

    @app.callback([Output('tsp-graph', 'children')],
                  [Input('memory', 'data'), Input('plot-switch', 'on')],
                  [State('memory', 'data')])
    def show_plot(_, plot, cache):
        if cache and plot:
            cities, edges = cache.values()

            output = list([html.H3(children='Plot'), comp.vbar()])
            output.append(comp.graph(cities, edges))
            return output,
        return None,

    @app.server.route('/tmp/solution')
    def download_solution():
        return flask.send_file('tmp/solution.txt',
                               mimetype='text',
                               attachment_filename='solution.txt',
                               as_attachment=True)

    @app.callback([Output('time-slider-output', 'children')],
                  [Input('time-slider', 'value')])
    def update_time(n):
        return [f'Max time {n} s']

    @app.callback([Output('simulations-slider-output', 'children')],
                  [Input('simulations-slider', 'value')])
    def update_simulations(n):
        return [f'Random walks per node {n}']

    @app.callback([Output('problem-type', 'children'), Output('upload-row', 'children')],
                  [Input('type-switch', 'on')])
    def update_view(old_solution):
        if old_solution:
            title = ['Upload solved problem']
            row = [
            html.Td(children=[
                comp.upload(idx='time-solution-input', name='Upload solution'),
                html.Div(id='time-output')],
                style={'width': '33%', 'vertical-align': 'top'}),

                html.Td(children=[
                    comp.upload(idx='city-input', name='Optional city matrix'),
                    html.Div(id='output-city')],
                    style={'width': '33%', 'vertical-align': 'top'}),

                html.Td(children=[
                    comp.upload(idx='paths-input', name='Upload paths'),
                    html.Div(id='paths-output')],
                    style={'width': '33%', 'vertical-align': 'top'}),
                ]
            return title, row

        title = ['Solve']
        row = [
            html.Td(children=[
                comp.upload(idx='city-input', name='City coordinates:'),
                html.Div(id='output-city')],
                style={'width': '33%', 'vertical-align': 'top'}),

            html.Td(children=[
                comp.upload(idx='paths-input', name='Paths information'),
                html.Div(id='paths-output')],
                style={'width': '33%', 'vertical-align': 'top'}),

            html.Td(children=[
                comp.upload(idx='time-solution-input', name='Magic .csv with time:'),
                html.Div(id='time-output')],
                style={'width': '33%', 'vertical-align': 'top'}),
        ]

        return title, row

    return app
