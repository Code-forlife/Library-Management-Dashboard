import dash
from dash import dcc, html, callback, Output, Input
import plotly.express as px
import plotly.graph_objs as go
import dash_bootstrap_components as dbc
import pandas as pd

dash.register_page(__name__, name='Overall Analysis')

# Read the data
df = pd.read_csv("BAPISE.csv")

# Calculate overall revenue, fine due, and fine waived
overall_revenue = df[df['Type'] == 'Return']['Fine'].sum()
fine_due = df[df['Type'] == 'Fine Due']['Fine'].sum()
fine_waived = df[df['Type'] == 'Fine Waived']['Fine'].sum()

# Calculate top 10 books by the number of issues
top_books = df[df['Type'] == 'Issue']['Title'].value_counts().head(10)

layout = html.Div(children=[
    html.Div(children=[
        html.Div(children=[
            html.H1("Overall Metrics", style={'textAlign': 'center'}),
            html.Div([
                html.H3(f"Overall Revenue: ₹{overall_revenue}"),
                html.H3(f"Fine Due: ₹{fine_due}"),
                html.H3(f"Fine Waived: ₹{fine_waived}")
            ], style={'display': 'flex', 'flex-direction': 'row', 'justify-content': 'space-around'})
        ], className='six columns'),
        
        html.Div(children=[
            html.H2("Top 10 Books by Issues", style={'textAlign': 'center'}),
            dcc.Graph(
                id='top-books-graph',
                figure={
                    'data': [
                        {
                            'x': top_books.index,
                            'y': top_books.values,
                            'type': 'bar',
                            'marker': {'color': 'rgb(26, 118, 255)'}
                        }
                    ],
                    'layout': {
                        # 'title': 'Top 10 Books by Issues',
                        'xaxis': {'title': 'Book Title', 'tickfont': {'color': 'white'}, 'titlefont': {'color': 'white'}},  # Change x-axis label color to white
                        'yaxis': {'title': 'Number of Issues', 'tickfont': {'color': 'white'}, 'titlefont': {'color': 'white'}},  # Change y-axis label color to white
                        'margin': {'l': 40, 'b': 40, 't': 50, 'r': 40},
                        'hovermode': 'closest',
                        'plot_bgcolor': '#000000',  # Change the background color to black
                        'paper_bgcolor': '#000000',  # Change the background color of the paper to black
                        'showgrid': False,  # Remove grid lines
                        'font': {'color': 'white'}  # Change text color to white
                    }
                }
            )
        ], className='six columns')
    ], className='row')
])
