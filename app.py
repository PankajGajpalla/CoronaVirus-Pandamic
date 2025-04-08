import numpy as np
import pandas as pd
import plotly.graph_objects as go
import dash
from dash import html, dcc
from dash.dependencies import Input, Output

external_stylesheets = [
    {
        'href': 'https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css',
        'rel': 'stylesheet',
        'integrity': 'sha348-MCw98/SFnGE8fJT3GXwEOngsV7Zt27NXFoaoApmYm81iuXoPKFOJwJ8ERdknLPMO',
        'crossorigin' : 'anonymous'

    }
]

patients = pd.read_csv("IndividualDetails.csv")

total = patients['current_status'].shape[0]
active = patients[patients['current_status'] == 'Hospitalized'].shape[0]
recovered = patients[patients['current_status'] == 'Recovered'].shape[0]
deaths = patients[patients['current_status'] == 'Deceased'].shape[0]

options = [
    {'label':'All', 'value': 'All'},
    {'label':'Hospitalized', 'value': 'Hospitalized'},
    {'label':'Recovered', 'value': 'Recovered'},
    {'label':'Deceased', 'value': 'Deceased'},
]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    html.H1("CoronaVirus Pandamic", style={'color': '#fff', 'text-align':'center'}),
    html.Div([
        html.Div([
            html.Div([
                html.Div([
                    html.H3("Total Cases", className='text-light'),
                    html.H4(total, className='text-light')
                ], className='card-body')
            ], className='card bg-danger')
        ], className='col-md-3'),
        html.Div([
            html.Div([
                html.Div([
                    html.H3("Active Cases", className='text-light'),
                    html.H4(active, className='text-light')
                ], className='card-body')
            ], className='card bg-info')
        ], className='col-md-3'),
        html.Div([
            html.Div([
                html.Div([
                    html.H3("Recovered", className='text-light'),
                    html.H4(recovered, className='text-light')
                ], className='card-body')
            ], className='card bg-warning')
        ], className='col-md-3'),
        html.Div([
            html.Div([
                html.Div([
                    html.H3("Deaths", className='text-light'),
                    html.H4(deaths, className='text-light')
                ], className='card-body')
            ], className='card bg-success')
        ], className='col-md-3')
    ], className='row'),
    html.Div([], className='row'),
    html.Div([
        html.Div([
            html.Div([
                html.Div([
                    dcc.Dropdown(
                        id='picker',
                        options=options,
                        value='All',
                        clearable=False,
                        style={'margin-bottom': '20px'}
                    ),
                    dcc.Graph(id='bar')
                ], className='card-body')
            ], className='card')
        ], className='col-md-12')
    ], className='row')
], style={'backgroundColor': '#000'}, className='container')


@app.callback(Output('bar', 'figure'), [Input('picker', 'value')])
def update_graph(type):
    if type == 'All':
        pbar = patients['detected_state'].value_counts().reset_index()
    else:
        npat = patients[patients['current_status'] == type]
        pbar = npat['detected_state'].value_counts().reset_index()

    return{
        'data': [go.Bar(x=pbar['detected_state'], y=pbar['count'])],
        'layout': go.Layout(
            title=' Kaido's State-wise Case Count',
            xaxis_title='State',
            yaxis_title='Number of Cases',
            plot_bgcolor='#f8f9fa'
        )
    }

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8080) #for reder it uses port 8080 and host..
