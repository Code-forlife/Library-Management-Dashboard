import dash
from dash import dcc, html, callback, Output, Input
import plotly.express as px
import pandas as pd


# dash.register_page(__name__, name='Author Analysis',path='/authoranalysis')

# Read the data
df = pd.read_csv("BAPISE.csv")
# # Remove non-numeric characters from the 'Fine' column and then convert to integers
# df['Fine'] = df['Fine'].str.replace('.', '').astype(int)

layout = html.Div([
    html.H1("Books Written by Authors"),
    html.Label("Select a author:"),
    dcc.Dropdown(
        id='author-dropdown',
        options=[{'label': author, 'value': author} for author in list(df['author'].unique())],
        value=df['author'].unique()[0]  # Default value,
    ),
    dcc.Graph(id='book-bar-chart')
])

@callback(
    Output('book-bar-chart', 'figure'),
    [Input('author-dropdown', 'value')]
)
def update_bar_chart(selected_author):
    filtered_data = df[df['author'] == selected_author]
    book_counts = filtered_data['Title'].value_counts()
    fig = px.bar(x=book_counts.index, y=book_counts.values, labels={'x': 'Book Title', 'y': 'Number of Books'},
                 title=f'Number of Books Written by {selected_author}')
    return fig
