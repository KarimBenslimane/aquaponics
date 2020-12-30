# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly
from dash.dependencies import Output, Input
import comms
import datetime

# TODO: ADD MESSAGE IF SENSOR IS CONNECTED
# TODO: ADD NAME TO GRAPH

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

phComms = comms.createConnection()

sensor = {
    'offline': 'block',
    'online': 'block'
}

if phComms:
    sensor['offline'] = 'none'
else:
    sensor['online'] = 'none'

data = {
    'ph': [],
    'time': [],
}
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.title = 'Aquaponics Monitor v0.1'

app.config.update({
    'requests_pathname_prefix': '/aqua/'
})

server = app.server

colors = {
    'background': '#111111',
    'text': '#FDCF76'
}

app.layout = html.Div(style={'backgroundColor': colors['background']}, children=[
    html.Div(
        html.H3(
            children='Aquaponics water quality monitor.',
            style={
                'textAlign': 'left',
                'color': colors['text']
            }
        ),
        style={'backgroundColor': '	#2F4F4F'}
    ),
    html.Div(
        children='pH sensor is offline',
        style={
            'textAlign': 'left',
            'color': '#F08080',
            'display': sensor['offline']
        }
    ),
    html.Div(
        children='pH sensor is online',
        style={
            'textAlign': 'left',
            'color': '#98FB98',
            'display': sensor['online']
        }
    ),
    html.Div([
        html.Div([
            html.H4('acidity', style={'textAlign': 'center'}),
            dcc.Graph(
                id='ph-update-graph'
            ),
            dcc.Interval(
                id='interval-component',
                interval=1 * 1000,
                n_intervals=0
            )
        ], className="six columns", style={'backgroundColor': colors['background']}),
        html.Div([
            html.H4('light', style={'textAlign': 'center'}),
            dcc.Graph(
                id='light-update-graph'
            )
        ], className="six columns", style={'backgroundColor': colors['background']}),
    ], style={'color': colors['text']})

])


@app.callback(Output('ph-update-graph', 'figure'),
              [Input('interval-component', 'n_intervals')])
def update_graph_live(n):
    if phComms:
        retrieved_data = comms.retrieveData(phComms)
        data['ph'].append(retrieved_data)
        data['time'].append(datetime.datetime.now())

    fig = plotly.tools.make_subplots(rows=1, cols=1, vertical_spacing=0.2)
    fig['layout']['margin'] = {
        'l': 40, 'r': 10, 'b': 40, 't': 10
    }
    fig['layout']['legend'] = {'x': 0, 'y': 1}
    fig['layout']['xaxis'] = {'title': 'Date'}
    fig['layout']['yaxis'] = {'title': 'Value'}
    fig['layout']['plot_bgcolor'] = colors['background']
    fig['layout']['paper_bgcolor'] = colors['background']
    fig['layout']['font'] = {'color': colors['text']}
    fig['layout']['showlegend'] = True

    fig.append_trace({
        'x': data['time'],
        'y': data['ph'],
        'name': 'acidity (pH)',
        'mode': 'lines+markers',
        'type': 'scatter',
    }, 1, 1)
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
