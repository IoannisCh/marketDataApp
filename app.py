import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import pandas as pd
import requests
import json

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
def update_graph_live(n_intervals, n_clicks, symbol):
    api_key = 'DE0TRYVU0UJ4BDPT'
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={symbol}&interval=1min&apikey={api_key}'
    
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an HTTPError if the HTTP request returned an unsuccessful status code
        
        data = response.json()
        
        # Print the API response for debugging
        print(json.dumps(data, indent=2))
        
        if 'Time Series (1min)' not in data:
            raise ValueError('API response does not contain expected data')
        
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

    except Exception as e:
        print(f"Error: {e}")
        return go.Figure(data=[], layout=go.Layout(title='Error'))

if __name__ == '__main__':
    app.run_server(debug=True)
