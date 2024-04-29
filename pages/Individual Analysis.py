import dash
from dash import dcc, html, callback, Output, Input
import plotly.express as px
import pandas as pd
import sqlite3

# Connect to SQLite database
conn = sqlite3.connect("student.db")

# Read data from SQLite database
df = pd.read_sql_query("SELECT * FROM students", conn)

# Close the database connection
conn.close()
# Remove non-numeric characters from the 'Fine' column and then convert to integers
df['Fine'] = df['Fine'].str.replace('.', '').astype(int)


# Convert date column to datetime with corrected format
df['Date'] = pd.to_datetime(df['Date'], format='%Y-%m-%d')

# Create Dash app
dash.register_page(__name__,path='/', name='Individual Analysis')

# Define unique UID values for dropdown options
uid_options = [{'label': uid, 'value': uid} for uid in df['UID'].unique()]

# Define app layout
layout = html.Div(style={'backgroundColor': '#000000', 'color': '#FFFFFF'}, children=[
    # Flexbox container for name, fine due, and dropdown
    html.Div(style={'display': 'flex', 'justifyContent': 'space-around', 'width': '100%'}, children=[
        # Name and Fine Due
        html.Div([
            html.Div(id='name-output', style={'textAlign': 'center', 'fontSize': 20}),
           
        ]),
         html.Div(id='fine-due-output', style={'textAlign': 'center', 'fontSize': 20}),
        # Dropdown for selecting UID
        dcc.Dropdown(id='uid-dropdown', options=uid_options, value=df['UID'].unique()[0],
                     style={'color': '#000000', 'width': '50%'}, className='dropdown-style')
    ]),
    
    # Pie chart of Type
    dcc.Graph(id='type-pie-chart'),
    
    # Bar chart of Title and issues
    dcc.Graph(id='title-bar-chart'),
    
    # Cumulative fine over time
    dcc.Graph(id='cumulative-fine'),
    
    # Title issued over time
    dcc.Graph(id='title-issued-over-time')
])

# Callback to update name and fine due based on dropdown selection
@callback(
    [Output('name-output', 'children'),
     Output('fine-due-output', 'children')],
    [Input('uid-dropdown', 'value')]
)
def update_name_and_fine_due(selected_uid):
    filtered_df = df[df['UID'] == selected_uid]
    total_fine_due = filtered_df[filtered_df['Type'] == 'Fine Due']['Fine'].sum()
    name = filtered_df['Name'].iloc[0]
    
    return f"Name: {name}", f"Fine Due: {total_fine_due}"

# Callback to update graphs based on dropdown selection
@callback(
    [Output('type-pie-chart', 'figure'),
     Output('title-bar-chart', 'figure'),
     Output('cumulative-fine', 'figure'),
     Output('title-issued-over-time', 'figure')],
    [Input('uid-dropdown', 'value')]
)
def update_graphs(selected_uid):
    filtered_df = df[df['UID'] == selected_uid]
    issue_df = filtered_df[filtered_df['Type'] == 'Issue']
    
    # Pie chart of Type
    pie_chart = px.pie(filtered_df, names='Type', title='Type Distribution')
    pie_chart.update_traces(marker=dict(colors=['#FFA500', '#008000', '#FF0000']))
    pie_chart.update_layout(title_font_color='#FFFFFF', paper_bgcolor='#000000', plot_bgcolor='#000000',
                             font=dict(color='#FFFFFF'), xaxis=dict(showgrid=False), yaxis=dict(showgrid=False))  # Update text color and remove grid lines
    
    # Bar chart of Title and issues
    bar_chart = px.bar(issue_df, x='Title', title='Titles Issued', color='Title')
    bar_chart.update_layout(title_font_color='#FFFFFF', paper_bgcolor='#000000', plot_bgcolor='#000000',
                             font=dict(color='#FFFFFF'), xaxis=dict(showgrid=False), yaxis=dict(showgrid=False))  # Update text color and remove grid lines
    
    # Cumulative fine over time
    cumulative_fine_chart = px.area(filtered_df, x='Date', y='Fine', title='Cumulative Fine Over Time')
    cumulative_fine_chart.update_traces(line=dict(color='#FFA500'))
    cumulative_fine_chart.update_layout(title_font_color='#FFFFFF', paper_bgcolor='#000000', plot_bgcolor='#000000',
                                         font=dict(color='#FFFFFF'), xaxis=dict(showgrid=False), yaxis=dict(showgrid=False))  # Update text color and remove grid lines
    
    # Title issued over time
    title_issued_chart = px.bar(issue_df, x='Date', title='Titles Issued Over Time', color='Title')
    title_issued_chart.update_layout(title_font_color='#FFFFFF', paper_bgcolor='#000000', plot_bgcolor='#000000',
                                      font=dict(color='#FFFFFF'), xaxis=dict(showgrid=False), yaxis=dict(showgrid=False))  # Update text color and remove grid lines
    
    return pie_chart, bar_chart, cumulative_fine_chart, title_issued_chart
