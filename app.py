import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import pandas as pd
import requests

app = dash.Dash(__name__)

app.layout = html.Div(children=[
    html.H1(children='Real-Time Market Data Dashboard'),

    dcc.Input(id='stock-symbol', value='AAPL', type='text'),
    html.Button(id='submit-button', n_clicks=0, children='Submit'),

    dcc.Graph(id='market-graph'),
    dcc.Interval(
        id='interval-component',
        interval=1*60000,  # in milliseconds
        n_intervals=0
    )
])

@app.callback(
    Output('market-graph', 'figure'),
    [Input('interval-component', 'n_intervals'),
     Input('submit-button', 'n_clicks')],
    [dash.dependencies.State('stock-symbol', 'value')]
)

import requests

def get_market_data(symbol):
    api_key = 'YOUR_API_KEY'
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={symbol}&interval=1min&apikey={api_key}'
    response = requests.get(url)
    data = response.json()
    return data


def update_graph_live(n_intervals, n_clicks, symbol):
    api_key = 'DE0TRYVU0UJ4BDPT'
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={symbol}&interval=1min&apikey={api_key}'
    response = requests.get(url)
    data = response.json()
    
    df = pd.DataFrame.from_dict(data['Time Series (1min)'], orient='index')
    df = df.astype(float)
    df.index = pd.to_datetime(df.index)
    df = df.sort_index()

    fig = go.Figure(
        data=[go.Scatter(
            x=df.index,
            y=df['1. open'],
            mode='lines+markers'
        )],
        layout=go.Layout(
            title=f'Real-Time Market Data for {symbol}',
            xaxis=dict(title='Time'),
            yaxis=dict(title='Price')
        )
    )

    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
