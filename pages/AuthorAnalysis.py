import dash
from dash import dcc, html, callback, Output, Input
import plotly.express as px
import pandas as pd
import sqlite3

dash.register_page(__name__, name='Author Analysis', path='/authoranalysis')

# Connect to SQLite database
conn = sqlite3.connect("student.db")

# Read data from SQLite database using SQL query
df = pd.read_sql_query("SELECT * FROM students", conn)

# Close the database connection
conn.close()

layout = html.Div([
    html.H1("Books Written by Authors"),
    html.Label("Select an author:"),
    html.Div(children=[

        dcc.Dropdown(
            id='author-dropdown',
            options=[{'label': author, 'value': author} for author in list(df['author'].unique())],
            value=df['author'].unique()[0],  # Default value,
            style={'width': '100%', 'color': 'black', 'align-item': 'center'}
        ),

    ], style={'display': 'flex', 'justify-content': 'center'}),
    dcc.Graph(id='book-bar-chart')
], style={'textAlign': 'center', 'height': '100vh', 'color': 'white'})

@callback(
    Output('book-bar-chart', 'figure'),
    [Input('author-dropdown', 'value')]
)
def update_bar_chart(selected_author):
    filtered_data = df[df['author'] == selected_author]
    book_counts = filtered_data['Title'].value_counts()
    fig = px.bar(x=book_counts.index, y=book_counts.values, labels={'x': 'Book Title', 'y': 'Number of Issues'},)
                #  title=f'Number of Books Written by {selected_author}')

    # Modify plot layout to remove grid
    fig.update_layout(
        plot_bgcolor='black',  # Set plot background color
        paper_bgcolor='rgba(0,0,0,0)',  # Set paper background color to transparent
        font=dict(color='white'),  # Set font color to white
        xaxis=dict(showgrid=False),  # Remove x-axis grid
        yaxis=dict(showgrid=False)  # Remove y-axis grid
    )

    return fig
