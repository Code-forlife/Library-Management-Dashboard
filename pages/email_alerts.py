import dash
from dash import dcc, html, Input, Output, State, callback
import pandas as pd
from datetime import datetime, timedelta
import smtplib
from email.message import EmailMessage
import dash_mantine_components as dmc
import sqlite3

dash.register_page(__name__, name='Email Alerts', path='/EMAIL_ALERTS')

# Connect to SQLite database
conn = sqlite3.connect("student.db")

# Load student data from SQLite database
student_data = pd.read_sql_query("SELECT * FROM students", conn)

# Close the database connection
conn.close()
# Remove non-numeric characters from the 'Fine' column and then convert to integers
student_data['Fine'] = student_data['Fine'].str.replace('.0', '').astype(int)


# Convert 'Date' column to datetime objects
student_data['Date'] = pd.to_datetime(student_data['Date'], format='%Y-%m-%d')

def send_alert(subject, body, to):
    msg = EmailMessage()
    msg.set_content(body)
    msg["subject"] = subject
    msg["to"] = to

    user = "bapdummy84@gmail.com"  # <-- Update here-------------------
    msg["from"] = user
    password = "rrzpxcupikginmmh"  # <-- Update here-------------------

    # set server parameters
    server = smtplib.SMTP("smtp.gmail.com", 587)  # create server variable
    server.starttls()
    server.login(user, password)
    server.send_message(msg)

    server.quit()

# Define app layout
layout = html.Div([
    html.H1("Student Fine Dashboard",style={'textAlign': 'center'}),
    html.Div([
        dcc.Input(id='start-date-input', type='text', placeholder='Start Date (YYYY-MM-DD)', style={'width': '200px'}),
        dcc.Input(id='end-date-input', type='text', placeholder='End Date (YYYY-MM-DD)', style={'width': '200px'}),
        html.Button('Filter Students', id='filter-button', n_clicks=0, style={'display': 'inline-block',
  'padding': '15px 25px',
  'font-size': '20px',
  'cursor': 'pointer',
  'width': '200px',
  'text-align': 'center',
  'text-decoration': 'none',
  'outline': 'none',
  'color': '#fff',
  'background-color': 'rgb(26, 118, 255)',
  'border': 'none',
  'border-radius': '5px',
  'box-shadow': '0 2px #999'}),
        html.Button("Send Email", id="send-email-button", n_clicks=0,style={'display': 'inline-block',
  'padding': '15px 25px',
  'font-size': '20px',
  'width': '200px',
  'cursor': 'pointer',
  'text-align': 'center',
  'text-decoration': 'none',
  'outline': 'none',
  'color': '#fff',
  'background-color': 'rgb(26, 118, 255)',
  'border': 'none',
  'border-radius': '5px',
  'box-shadow': '0 2px #999'})
    ],style={'display': 'flex', 'justifyContent': 'space-around', 'margin': '20px'}),
    
    html.Div(id='email-status'),
    html.Table([
        html.Thead([
            html.Tr([
                html.Th("Name", style={'padding': '10px', 'border': '1px solid white'}),
                html.Th("UID", style={'padding': '10px', 'border': '1px solid white'}),
                html.Th("Fine Due", style={'padding': '10px', 'border': '1px solid white'}),
                html.Th("Duration (days)", style={'padding': '10px', 'border': '1px solid white'}),
                html.Th("Email Address", style={'padding': '10px', 'border': '1px solid white'}),
            ])
        ]),
        html.Tbody(id='student-table')
    ], style={'border': '1px solid white', 'align': 'center', 'width': '100%', 'textAlign': 'center'})
], style={'height': '100vh', 'backgroundColor': '#000000', 'color': '#FFFFFF'})

# Callback to update student table
@callback(
    Output('student-table', 'children'),
    Input('filter-button', 'n_clicks'),
    State('start-date-input', 'value'),
    State('end-date-input', 'value')
)
def update_student_table(n_clicks, start_date, end_date):
    if n_clicks > 0 and start_date and end_date:
        try:
            start_date = datetime.strptime(start_date, '%Y-%m-%d')
            end_date = datetime.strptime(end_date, '%Y-%m-%d')
            overdue_students = student_data[(student_data['Type'] == 'Fine Due') & (student_data['Date'] >= start_date) & (student_data['Date'] <= end_date)]

            rows = []
            for index, student in overdue_students.iterrows():
                duration = (datetime.now() - student['Date']).days
                rows.append(
                    html.Tr([
                        html.Td(student['Name'], style={'padding': '10px', 'border': '1px solid white'}),
                        html.Td(student['UID'], style={'padding': '10px', 'border': '1px solid white'}),
                        html.Td(f"₹ {student['Fine']}", style={'padding': '10px', 'border': '1px solid white'}),
                        html.Td(duration, style={'padding': '10px', 'border': '1px solid white'}),
                        html.Td(student['Email'], style={'padding': '10px', 'border': '1px solid white'}),
                    ])
                )
            return rows
        except ValueError:
            return [html.Tr([html.Td("Invalid date format. Please use YYYY-MM-DD format for dates.")])]
    else:
        return []

# Callback to send email and update status
@callback(
    Output('email-status', 'children'),
    Input('send-email-button', 'n_clicks'),
    State('student-table', 'children'),
    State('start-date-input', 'value'),
    State('end-date-input', 'value')
)
def send_email_to_students(n_clicks, student_table, start_date, end_date):
    if n_clicks > 0:
        # Extract the email addresses of the students shown in the dashboard
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
        end_date = datetime.strptime(end_date, '%Y-%m-%d')
        overdue_students = student_data[(student_data['Type'] == 'Fine Due') & (student_data['Date'] >= start_date) & (student_data['Date'] <= end_date)]

        for index, student in overdue_students.iterrows():
            subject = 'Overdue Fine Notification'
            body = f"Dear Student,\n\nThis is to inform you that you have an overdue fine. Please settle the fine at your earliest convenience.\n\nRegards,\nThe Library Team"
            send_alert(subject, body, student['Email'])

        return "Emails sent successfully."
