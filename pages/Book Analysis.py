import dash
from dash import dcc, html, callback, Output, Input
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import pandas as pd
import dash_bootstrap_components as dbc
import calendar
import sqlite3
# Connect to SQLite database
conn = sqlite3.connect("student.db")

# Read data from SQLite database
df = pd.read_sql_query("SELECT * FROM students", conn)
# Close the database connection
conn.close()
# Remove non-numeric characters from the 'Fine' column and then convert to integers
df['Fine'] = df['Fine'].str.replace('.', '').astype(int)

dash.register_page(__name__, name='Book Analysis',path='/bookanalysis')

# Convert date column to datetime with corrected format
df['Date'] = pd.to_datetime(df['Date'], format='%Y-%m-%d')
df['Year'] = df['Date'].dt.year
df['Month'] = df['Date'].dt.month

# Map month numbers to month names
df['Month'] = df['Month'].apply(lambda x: calendar.month_abbr[x])

# Group by month and count the number of issues
issues_per_month = df[df['Type'] == 'Issue'].groupby('Month').size()

layout = html.Div([
    html.H1("Library Analysis Dashboard"),
    html.Label("Select a book:"),
    dcc.Dropdown(
        id='book-dropdown',
        options=[{'label': book, 'value': book} for book in df['Title'].unique()],
        value=df['Title'].unique()[0]  # Default value,
    ),
    dbc.Row([
        dbc.Col(dcc.Graph(id='fines-graph'), width=6),
        dbc.Col(dcc.Graph(id='issues-graph'), width=6)
    ]),
    dbc.Row([
        dbc.Col(dcc.Graph(id='issues-month'), width=6),
        dbc.Col(dcc.Graph(id='fines-month'), width=6)
    ]),
],style={'backgroundColor': '#000000', 'height': '100vh', 'color': 'black'})


@callback(
    Output('fines-graph', 'figure'),
    [Input('book-dropdown', 'value')]
)
def update_fines_graph(selected_book):
    filtered_df = df[df['Title'] == selected_book]
    total_fines_per_month = filtered_df.groupby(['Year', 'Month'])['Fine'].sum().reset_index()
    
    # Create a new column combining year and month for x-axis labeling
    total_fines_per_month['Year_Month'] = total_fines_per_month['Year'].astype(str) + '-' + total_fines_per_month['Month'].astype(str)
    
    return {
        'data': [go.Scatter(x=total_fines_per_month['Year_Month'], y=total_fines_per_month['Fine'], mode='lines')],
        'layout': go.Layout(
            title=f"Total Fines per Month for {selected_book}",
            xaxis={'title': 'Month'},
            yaxis={'title': 'Total Fines'},
            plot_bgcolor='black',  # Set plot background color
            paper_bgcolor='rgba(0,0,0,0)',  # Set paper background color to transparent
            font={'color': 'white'}  # Set font color to white
        )
    }


@callback(
    Output('issues-graph', 'figure'),
    [Input('book-dropdown', 'value')]
)
def update_issues_graph(selected_book):
    filtered_df = df[(df['Title'] == selected_book) & (df['Type'] == 'Issue')]
    issues_per_month = filtered_df.groupby(['Year', 'Month']).size().reset_index(name='Issue_Count')
    
    # Create a new column combining year and month for x-axis labeling
    issues_per_month['Year_Month'] = issues_per_month['Year'].astype(str) + '-' + issues_per_month['Month'].astype(str)
    
    return {
        'data': [go.Scatter(x=issues_per_month['Year_Month'], y=issues_per_month['Issue_Count'], mode='lines')],
        'layout': go.Layout(
            title=f"Issues per Month for {selected_book}",
            xaxis={'title': 'Month'},
            yaxis={'title': 'Number of Issues'},
            plot_bgcolor='black',  # Set plot background color
            paper_bgcolor='rgba(0,0,0,0)',  # Set paper background color to transparent
            font={'color': 'white'}  # Set font color to white
        )
    }

@callback(
    Output('issues-month', 'figure'),
    [Input('book-dropdown', 'value')]
)
def update_issues_graph_month(selected_book):
    filtered_df = df[(df['Title'] == selected_book) & (df['Type'] == 'Issue')]
    issues_per_month = filtered_df.groupby('Month').size()

    # Sort months chronologically
    sorted_months = sorted(issues_per_month.index, key=lambda m: list(calendar.month_abbr).index(m))
    
    return {
        'data': [go.Scatter(
            x=sorted_months,
            y=issues_per_month[sorted_months],
            mode='lines+markers',
            line=dict(color='rgb(26, 118, 255)', width=2),
            marker=dict(color='rgb(26, 118, 255)', size=8)
        )],
        'layout': go.Layout(
            title=f"Issue Count per Month for {selected_book}",
            xaxis=dict(title='Month', tickfont=dict(color='white'), titlefont=dict(color='white'), categoryorder='array', categoryarray=sorted_months, showgrid=False),
            yaxis=dict(title='Number of Issues', tickfont=dict(color='white'), titlefont=dict(color='white'), showgrid=False),
            plot_bgcolor='#000000',
            paper_bgcolor='#000000',
            font=dict(color='white')
        )
    }

@callback(
    Output('fines-month', 'figure'),
    [Input('book-dropdown', 'value')]
)
def update_fines_graph_month(selected_book):
    filtered_df = df[(df['Title'] == selected_book)]
    fines_per_month = filtered_df.groupby('Month')['Fine'].sum()

    # Sort months chronologically
    sorted_months = sorted(fines_per_month.index, key=lambda m: list(calendar.month_abbr).index(m))
    
    return {
        'data': [go.Scatter(
            x=sorted_months,
            y=fines_per_month[sorted_months],
            mode='lines+markers',
            line=dict(color='rgb(26, 118, 255)', width=2),
            marker=dict(color='rgb(26, 118, 255)', size=8)
        )],
        'layout': go.Layout(
            title=f"Total Fines per Month for {selected_book}",
            xaxis=dict(title='Month', tickfont=dict(color='white'), titlefont=dict(color='white'), categoryorder='array', categoryarray=sorted_months, showgrid=False),
            yaxis=dict(title='Total Fines', tickfont=dict(color='white'), titlefont=dict(color='white'), showgrid=False),
            plot_bgcolor='#000000',
            paper_bgcolor='#000000',
            font=dict(color='white')
        )
    }

