import dash
from dash import dcc, html, callback, Output, Input
import plotly.express as px
import plotly.graph_objs as go
import dash_bootstrap_components as dbc
import pandas as pd
import calendar

dash.register_page(__name__, name='Overall Analysis')

# Read the data
df = pd.read_csv("BAPISE.csv")

# Remove all UIDs that start with 'U' or 'u'
df = df[~df['UID'].astype(str).str.startswith(('U', 'u'))]

# Calculate overall revenue, fine due, and fine waived
overall_revenue = df[df['Type'] == 'Return']['Fine'].sum()
fine_due = df[df['Type'] == 'Fine Due']['Fine'].sum()
fine_waived = df[df['Type'] == 'Fine Waived']['Fine'].sum()

# Calculate top 10 books by the number of issues
top_books = df[df['Type'] == 'Issue']['Title'].value_counts().head(10)

# Extract month from the 'Date' column
df['Date'] = pd.to_datetime(df['Date'])
df['Month'] = df['Date'].dt.month

# Map month numbers to month names
df['Month'] = df['Month'].apply(lambda x: calendar.month_abbr[x])

# Group by month and count the number of issues
issues_per_month = df[df['Type'] == 'Issue'].groupby('Month').size()

# Sort months chronologically
sorted_months = sorted(issues_per_month.index, key=lambda m: list(calendar.month_abbr).index(m))

# Create a line graph to display issue count per month
issue_per_month_fig = go.Figure()
issue_per_month_fig.add_trace(go.Scatter(
    x=sorted_months,
    y=issues_per_month[sorted_months],
    mode='lines+markers',
    line=dict(color='rgb(26, 118, 255)', width=2),
    marker=dict(color='rgb(26, 118, 255)', size=8)
))
issue_per_month_fig.update_layout(
    # title='Issue Count per Month',
    xaxis=dict(title='Month', tickfont=dict(color='white'), titlefont=dict(color='white'), categoryorder='array', categoryarray=sorted_months, showgrid=False),
    yaxis=dict(title='Number of Issues', tickfont=dict(color='white'), titlefont=dict(color='white'), showgrid=False),
    plot_bgcolor='#000000',
    paper_bgcolor='#000000',
    font=dict(color='white')
)

# Extract year from UID
df['Year'] = df['UID'].astype(str).str[:4]

# Group by year and count the number of students
students_per_year = df.groupby('Year')['UID'].nunique()

# Filter out "BH00" category and rename other categories
filtered_students_per_year = students_per_year.drop('BH00')
renamed_categories = {
    '2023': 'First Year',
    '2022': 'Second Year',
    '2021': 'Third Year',
    '2020': 'Fourth Year'
}

# Create a pie chart to display the distribution of students by year
students_per_year_fig = go.Figure()
students_per_year_fig.add_trace(go.Pie(
    labels = [renamed_categories.get(category, category) for category in filtered_students_per_year.index],
    values=filtered_students_per_year.values,
    marker=dict(colors=px.colors.qualitative.Pastel),
    hole=0.5
))
students_per_year_fig.update_layout(
    # title='Distribution of Students by Year',
    plot_bgcolor='#000000',
    paper_bgcolor='#000000',
    font=dict(color='white')
)
# Filter out "Issue" and "Reissue" categories
filtered_df = df[~df['Type'].isin(['Issue', 'ReIssue'])]

# Group by month and type of fine, and sum the fine amount for each combination
fine_per_month_type = filtered_df.groupby(['Month', 'Type'])['Fine'].sum().unstack()

# Sort months chronologically
sorted_months = sorted(df['Month'].unique(), key=lambda m: list(calendar.month_abbr).index(m))

# Create a line graph to display fine amount per month and type of fine
fine_per_month_type_fig = go.Figure()

for fine_type in fine_per_month_type.columns:
    fine_per_month_type_fig.add_trace(go.Scatter(
        x=sorted_months,
        y=fine_per_month_type[fine_type][sorted_months],
        mode='lines+markers',
        name=fine_type,
        line=dict(width=2),
        marker=dict(size=8)
    ))

fine_per_month_type_fig.update_layout(
    # title='Fine Amount per Month by Type',
    xaxis=dict(title='Month', tickfont=dict(color='white'), titlefont=dict(color='white'), categoryorder='array', categoryarray=sorted_months, showgrid=False),
    yaxis=dict(title='Fine Amount', tickfont=dict(color='white'), titlefont=dict(color='white'), showgrid=False),
    plot_bgcolor='#000000',
    paper_bgcolor='#000000',
    font=dict(color='white')
)
# Group by year and sum the fine amount for each year
fine_per_year = df.groupby('Year')['Fine'].sum()
# Filter out "BH00" category and rename other categories
fine_per_year = fine_per_year.drop('BH00')
# Create a pie chart to display the distribution of fines by year
fine_per_year_fig = go.Figure()
fine_per_year_fig.add_trace(go.Pie(
    labels = [renamed_categories.get(category, category) for category in filtered_students_per_year.index],
    values=fine_per_year.values,
    marker=dict(colors=px.colors.qualitative.Pastel),
    hole=0.5
))
fine_per_year_fig.update_layout(
    # title='Distribution of Fines by Year',
    plot_bgcolor='#000000',
    paper_bgcolor='#000000',
    font=dict(color='white')
)


# Add the pie chart to the layout
layout = html.Div(children=[
    html.Div(children=[
        html.Div(children=[
            html.H1("Overall Metrics", style={'textAlign': 'center', 'margin-top': '50px'}),
            html.Div([
                html.H3(f"Overall Revenue: ₹{overall_revenue}"),
                html.H3(f"Fine Due: ₹{fine_due}"),
                html.H3(f"Fine Waived: ₹{fine_waived}")
            ], style={'display': 'flex', 'flex-direction': 'row', 'justify-content': 'space-around'})
        ], className='six columns'),
        
        html.Div(children=[
            html.H2("Top 10 Books by Issues", style={'textAlign': 'center', 'margin-top': '50px'}),
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
                        'xaxis': {'title': 'Book Title', 'tickfont': {'color': 'white'}, 'titlefont': {'color': 'white'}},
                        'yaxis': {'title': 'Number of Issues', 'tickfont': {'color': 'white'}, 'titlefont': {'color': 'white'}},
                        'margin': {'l': 40, 'b': 40, 't': 50, 'r': 40},
                        'hovermode': 'closest',
                        'plot_bgcolor': '#000000',
                        'paper_bgcolor': '#000000',
                        'font': {'color': 'white'}
                    }
                }
            )
        ], className='six columns')
    ], className='row'),
    # New graph displaying issue count per month
    html.Div(children=[
        html.H2("Issue Count per Month", style={'textAlign': 'center', 'margin-top': '50px'}),
        dcc.Graph(
            id='issue-per-month-graph',
            figure=issue_per_month_fig
        )
    ], className='twelve columns'),
    dbc.Row([
            dbc.Col(
                html.Div(children=[
                    html.H2("Distribution of Students by Year", style={'textAlign': 'center', 'margin-top': '50px'}),
                    dcc.Graph(
                        id='students-per-year-graph',
                        figure=students_per_year_fig
                    )
                ]),
                width=6  # Half of the row width
            ),
            dbc.Col(
                html.Div(children=[
                    html.H2("Distribution of Fines by Year", style={'textAlign': 'center', 'margin-top': '50px'}),
                    dcc.Graph(
                        id='fines-per-year-graph',
                        figure=fine_per_year_fig
                    )
                ]),
                width=6  # Half of the row width
            )
        ]),
    html.Div(children=[
        html.H2("Fine Amount per Month by Type", style={'textAlign': 'center', 'margin-top': '50px'}),
        dcc.Graph(
            id='fine-per-month-type-graph',
            figure=fine_per_month_type_fig
        )
    ], className='twelve columns')
        
], style={'backgroundColor': '#000000', 'height': '100%'})
