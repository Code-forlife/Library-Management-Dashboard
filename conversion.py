import csv
import sqlite3

# Function to create SQLite table
def create_table(cursor, table_name, headers):
    headers_str = ', '.join(headers)
    cursor.execute(f"CREATE TABLE {table_name} ({headers_str})")

# Function to insert data into SQLite table
def insert_data(cursor, table_name, data):
    placeholders = ', '.join(['?' for _ in range(len(data[0]))])
    cursor.executemany(f"INSERT INTO {table_name} VALUES ({placeholders})", data)

# CSV file path
csv_file = 'student_data_with_email.csv'
# SQLite database path
sqlite_db = 'student.db'
# Table name in SQLite database
table_name = 'students'

# Open CSV file and read data
with open(csv_file, 'r') as file:
    reader = csv.reader(file)
    headers = next(reader)  # Assuming the first row contains headers
    data = list(reader)

# Connect to SQLite database
conn = sqlite3.connect(sqlite_db)
cursor = conn.cursor()

# Create table
create_table(cursor, table_name, headers)

# Insert data into table
insert_data(cursor, table_name, data)

# Commit changes and close connection
conn.commit()
conn.close()

print("CSV data has been successfully converted to SQLite database.")