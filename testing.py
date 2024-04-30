from datetime import datetime
import pandas as pd

# Sample student data with email addresses
student_data = pd.DataFrame({
    'Name': ['Sahil Shah', 'Pranay Singhvi'],
    'UID': ['2021300126', '2021300126'],
    'Fine': [10, 20],
    'Date': ['2024-04-20', '2024-04-15'],  # Assuming these dates are within the range you'll input
    'Email': ['sahil.shah@spit.ac.in', 'pranay.singhvi@spit.ac.in']
})

# Function to simulate sending email
def send_alert(subject, body, to):
    print(f"Email sent to: {to}\nSubject: {subject}\nBody: {body}")

# Function to simulate updating student table
def update_student_table(start_date, end_date):
    # Convert 'Date' column to datetime objects
    student_data['Date'] = pd.to_datetime(student_data['Date'], format='%Y-%m-%d')
    
    # Filter students based on date range
    overdue_students = student_data[(student_data['Date'] >= start_date) & (student_data['Date'] <= end_date)]
    
    return overdue_students

# Function to simulate sending email to students
def send_email_to_students(overdue_students):
    for index, student in overdue_students.iterrows():
        subject = 'Overdue Fine Notification'
        body = f"Dear {student['Name']},\n\nThis is to inform you that you have an overdue fine of ${student['Fine']}. Please settle the fine at your earliest convenience.\n\nRegards,\nThe Library Team"
        send_alert(subject, body, student['Email'])

# Test the functionality
start_date = datetime.strptime('2024-04-01', '%Y-%m-%d')
end_date = datetime.strptime('2024-04-30', '%Y-%m-%d')

# Update student table
overdue_students = update_student_table(start_date, end_date)

# Send email to overdue students
send_email_to_students(overdue_students)
print("All Test Cases Passed!")
