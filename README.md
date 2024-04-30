# Library Management Dashboard

This project is a web-based dashboard built using Dash and Plotly, designed to visualize and manage library data. It empowers you to gain valuable insights into library usage, user trends, and book popularity.

### Key Features

* **Individual Analysis:** Gain a comprehensive view of specific users, including:
    * **Transaction Breakdown:** Visualize the distribution of transaction types (borrowing, returning, fines) for a user using a pie chart.
    * **Fine Distribution:** Analyze fine trends over time with a histogram, helping identify frequent defaulters.
    * **Book Issuance History:** Explore a histogram that reveals which books a user has borrowed and the frequency.
* **Overall Analysis:** Understand library usage patterns on a broader scale:
    * **Top 10 Issued Books:** Identify the most popular books based on their total issuance count (histogram).
    * **Monthly Issuance Trends:** Uncover seasonal trends or changes in borrowing patterns over time with a line chart.
    * **Issuance by Year of Study:** Gain insights into which student groups borrow the most books and generate the highest fines (bar chart).
    * **Monthly Fine Variations:** Analyze the fluctuation of fines due, fines paid, and fines waived off across months (line chart).
* **Book Analysis:** Assess book popularity and usage:
    * **Monthly Book Issuance:** Uncover trends in book demand throughout the year (bar chart).
    * **Book Issuance vs. Monthly Fines:** Explore the relationship between book issuance and fines paid per month (line chart), potentially revealing semesters with higher borrowing and overdue occurrences.
* **Author Analysis:** Drill down into specific authors and their works:
    * **Author Book Popularity:** View a histogram for each author, showing the individual issuance count of their books.
* **Email Alerts:** Manage user communication:
    * **Fine Delinquency Management:** Filter students by specific date ranges, identify unpaid fines, and send email alerts for timely collections.
* **Variety Analysis:** Explore book category trends:
    * **3D Borrow Count Distribution:** Visualize the distribution of borrowed books by category and year in a 3D plot. This helps identify shifts in borrowing patterns between years (e.g., more diverse categories in 2024 compared to 2023).

### Technologies

* **Dash:** A Python framework for building analytical web apps [https://dash.plotly.com/](https://dash.plotly.com/)
* **Plotly:** A library for creating interactive visualizations in Python [https://plotly.com/python/](https://plotly.com/python/)

### Installation

1. Clone this repository:

   ```bash
   git clone https://github.com/Code-forlife>/Library-Management-Dashboard.git
   ```

2. Install required dependencies:

   ```bash
   pip install dash dash-renderer dash-core-components dash-html-components plotly wordcloud
   ```

### Usage

1. Run the application:

   ```bash
   python app.py
   ```

2. Open http://127.0.0.1:8050/ in your web browser to access the dashboard.

**Note:** This is a basic example. Data connection may require additional configuration based on your chosen database. Explore and customize the `app.py` script to tailor the visualizations and functionalities of the dashboard to your specific needs.

### Contributing

Sahil Shah, Pranay Singhvi(DesiCoder), Sarthak Gharat, Shivam Kamble, Palaash Jain

### License

This project is licensed under the MIT License. See the LICENSE file for details.
