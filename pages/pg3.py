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

# Create 3D scatter plot
scatter_3d = go.Scatter3d(
    x=borrow_count_year_title['Date'],
    y=borrow_count_year_title['Title'],
    z=borrow_count_year_title['Borrow Count'],
    mode='markers',
    marker=dict(
        size=10,
        color=borrow_count_year_title['Date'],  
        colorscale='Viridis',  
        opacity=0.8,
        line=dict(color='rgb(255,255,255)', width=0.5)  # Color and width of marker outline
    ),
    text=borrow_count_year_title['Borrow Count'].astype(str) + ' times borrowed',  
    hoverinfo='text'
)

# Define layout
layout = go.Layout(
    title='Borrow Count for Each Year and Title',
    scene=dict(
        xaxis=dict(title='Year', gridcolor='rgba(0,0,0,0)', linecolor='rgba(0,0,0,0)'),  # Remove grid lines
        yaxis=dict(title='Book Title', gridcolor='rgba(0,0,0,0)', linecolor='rgba(0,0,0,0)'),  # Remove grid lines
        zaxis=dict(title='Borrow Count', gridcolor='rgba(0,0,0,0)', linecolor='rgba(0,0,0,0)'),  # Remove grid lines
        xaxis_title_font=dict(color='white'),  # Change x-axis title color to white
        yaxis_title_font=dict(color='white'),  # Change y-axis title color to white
        zaxis_title_font=dict(color='white')   # Change z-axis title color to white
    ),
    margin=dict(l=0, r=0, b=0, t=40),
    paper_bgcolor='black',  # Background color of the plot
    plot_bgcolor='black' ,
    font=dict(color='white')      # Background color of the plot area
)

# Combine plot and layout in a figure
fig = go.Figure(data=[scatter_3d], layout=layout)

# Define app layout with CSS style
layout = html.Div(style={'backgroundColor': 'black'}, children=[
    html.H1("Library Dashboard", style={'color': 'white'}),  # Title with white text color
    dcc.Graph(id='3d-scatter-plot', figure=fig)
])

