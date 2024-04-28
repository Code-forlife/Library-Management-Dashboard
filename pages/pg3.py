import pandas as pd
import plotly.graph_objs as go
import dash
from dash import dcc, html

# Read the dataset
df = pd.read_csv('BAPISE.csv')
dash.register_page(__name__, name='Overall')

# Convert 'Date' column to datetime format
df['Date'] = pd.to_datetime(df['Date'], format='%d-%m-%y')

# Group by year and title to calculate borrow count
borrow_count_year_title = df.groupby([df['Date'].dt.year, 'Title']).size().reset_index(name='Borrow Count')

# Filter borrow_count_year_title DataFrame to show only points with borrow count more than 5
borrow_count_year_title_filtered = borrow_count_year_title[borrow_count_year_title['Borrow Count'] > 5]

def diction(title = None):
    return dict(
        title=title,
        showbackground=True, 
        backgroundcolor="rgb(10,10,10)", 
        gridcolor="rgb(0, 0, 0,0)",  
        gridwidth=0,
        zeroline=False
    )

# Create 3D scatter plot with filtered data
scatter_3d = go.Scatter3d(
    x=borrow_count_year_title_filtered['Date'],
    y=borrow_count_year_title_filtered['Title'],
    z=borrow_count_year_title_filtered['Borrow Count'],
    mode='markers',
    marker=dict(
        size=10,
        color=borrow_count_year_title_filtered['Date'],  
        colorscale='Viridis',  
        opacity=0.8,
        line=dict(color='rgb(255,255,255)', width=0.5)  
    ),
    text=borrow_count_year_title_filtered['Borrow Count'].astype(str) + ' times borrowed',  
    hoverinfo='text'
)

layout = go.Layout(
    title='Borrow Count for Each Year and Title',
    scene=dict(
        xaxis=diction('Year'), 
        yaxis=diction(),  
        zaxis=diction('Borrow Count'),  
        xaxis_title_font=dict(color='white'),  
        yaxis_title_font=dict(color='white'),  
        zaxis_title_font=dict(color='white')
    ),
    margin=dict(l=0, r=0, b=0, t=40),
    paper_bgcolor='black',
    plot_bgcolor='black',
    font=dict(color='white'),
    hoverlabel=dict(bgcolor='black', font=dict(color='white')),
    coloraxis=dict(colorbar=dict(title='Year', tickfont=dict(color='blue'))) 
)

# Combine plot and layout in a figure
fig = go.Figure(data=[scatter_3d], layout=layout)

# Define app layout with CSS style
layout = html.Div(style={'backgroundColor': 'black', 'height': '100vh'}, children=[
    html.H1("Library Dashboard", style={'color': 'white'}),  
    dcc.Graph(id='3d-scatter-plot', figure=fig)
])
