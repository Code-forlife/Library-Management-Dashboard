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

def diction(title=None):
    return dict(
        title=title,
        showbackground=True, 
        backgroundcolor="rgb(10,10,10)", 
        gridcolor="rgb(0, 0, 0,0)",  
        gridwidth=0,
        zeroline=False,
    )

# Create a list of unique titles
unique_titles = borrow_count_year_title['Title'].unique()

# Create a trace for each unique title
scatter_traces = []
for title in unique_titles:
    filtered_data = borrow_count_year_title[borrow_count_year_title['Title'] == title]
    trace = go.Scatter3d(
        x=filtered_data['Date'],
        y=[title] * len(filtered_data),  # Assign the same y-value for each point in the trace
        z=filtered_data['Borrow Count'],
        mode='markers',
        name=title,  # Use the title as the name for the legend
        marker=dict(
            size=10,
            opacity=1,
        ),
        text=filtered_data['Borrow Count'].astype(str) + ' times borrowed',  
        hoverinfo='text'
    )
    scatter_traces.append(trace)

layout = go.Layout(
    title='Borrow Count for Each Year and Title',
    scene=dict(
        xaxis=diction('Year'), 
        # Remove y-axis title
        yaxis=diction('Books'),  
        zaxis=diction('Borrow Count'),  
        xaxis_title_font=dict(color='white'),  
        # Remove y-axis title font color
        yaxis_title_font=dict(color='white'),  
        zaxis_title_font=dict(color='white')
    ),
    paper_bgcolor='black',
    plot_bgcolor='black',
    height=800,  # Adjust the height of the plot
    width=1600,  # Adjust the width of the plot
    font=dict(color='white'),
    hoverlabel=dict(bgcolor='black', font=dict(color='white')),
)

# Combine plot traces and layout in a figure
fig = go.Figure(data=scatter_traces, layout=layout)

# Remove y-axis tick labels
fig.update_layout(scene=dict(yaxis=dict(showticklabels=False)))

# Remove decimal years in the x-axis tickvals and ticktext
fig.update_layout(scene=dict(xaxis=dict(
    tickvals=df['Date'].dt.year.unique(),  # Set tick values to integer years
    ticktext=df['Date'].dt.year.unique().astype(int)  # Set tick text to integer years
)))

# Define app layout with CSS style
layout = html.Div(style={'backgroundColor': 'black', 'height': '100vh'}, children=[
    dcc.Graph(id='3d-scatter-plot', figure=fig)
])
