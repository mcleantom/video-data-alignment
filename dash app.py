# -*- coding: utf-8 -*-
"""
Created on Thu Sep 24 16:18:41 2020

@author: Rastko
"""

import base64
import datetime
import io

import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import webbrowser
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os

if not os.path.exists("images"):
    os.mkdir("images")

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

fig = make_subplots(rows=3, cols=1, 
                    shared_xaxes=True,
                    vertical_spacing=0.02)

fig.add_trace(go.Scatter(x=[0, 1, 2], y=[10, 11, 12]),
              row=3, col=1)

fig.add_trace(go.Scatter(x=[2, 3, 4], y=[100, 110, 120]),
              row=2, col=1)

fig.add_trace(go.Scatter(x=[3, 4, 5], y=[1000, 1100, 1200]),
              row=1, col=1)

fig.update_layout(height=1080, width=1980/2)
fig.write_image("images/fig1.png")

app.layout = html.Div([
    dcc.Upload(
        id='upload-image',
        children=html.Div([
            'Upload Videos: Drag and Drop or ',
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
        # Allow multiple files to be uploaded
        multiple=True
    ),
    html.Div(id='hidden-div'),  # , style={'display':'none'}
    dcc.Slider(
       id='video-slider',
       min=0,
       max=30,
       step=0.1,
       value=0
    ),
    dcc.Graph(figure=fig),
    dcc.Graph(figure=fig)
])


def parse_contents(contents, filename, date):
    return html.Div([
        html.H5(filename),
#        html.H6(datetime.datetime.fromtimestamp(date)),
#        html.Video(src=contents, controls=True, id="video1"),
#        html.Div(id="video1time")
#        html.Hr(),
#        html.Div('Raw Content'),
#        html.Pre(contents[0:200] + '...', style={
#            'whiteSpace': 'pre-wrap',
#            'wordBreak': 'break-all'
#        })
    ])


@app.callback(Output('hidden-div', 'children'),
              [Input('upload-image', 'contents')],
              [State('upload-image', 'filename'),
               State('upload-image', 'last_modified')])
def update_output(list_of_contents, list_of_names, list_of_dates):
    if list_of_contents is not None:
        children = [
            parse_contents(c, n, d) for c, n, d in
            zip(list_of_contents, list_of_names, list_of_dates)]
        return children

if __name__ == '__main__':
#    webbrowser.open("http://127.0.0.1:8050/", new=0, autoraise=True)
    app.run_server(debug=True)
    