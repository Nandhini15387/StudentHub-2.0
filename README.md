StudentHub 2.0 — Student Management System

A web-based Student Management System built using Python, Flask, SQLite, HTML, and CSS. It helps users manage student records through a simple dashboard with search, filtering, sorting, analytics, and CSV export.

Features

- Dashboard Analytics: View total students, average marks, top student, and department count.
- Student Management: Add, view, edit, and delete student records.
- Search: Search students by name or roll number.
- Filtering: Filter records by department.
- Sorting: Sort by name, roll number, year, marks, or newest records.
- Performance Indicators: Categorize marks into performance levels.
- Department Overview: View student counts and average marks by department.
- CSV Export: Export student records to a CSV file.
- Input Validation: Validate required fields, duplicate roll numbers, academic year, and marks.
- SQLite Database: Store records persistently.
- Responsive Design: Use the dashboard on desktop and mobile-sized screens.

Technologies Used

- Python
- Flask
- SQLite
- HTML5
- CSS3
- CSV

Project Structure

Student ManagementSystem/
├── app.py
├── requirements.txt
├── README.md
├── students.db
├── templates/
│   ├── index.html
│   └── edit.html
└── static/
    └── style.css

The database file is created by the application when it initializes. Do not commit a database containing private student information.

Installation and Setup

1. Install Python

Install Python 3 if it is not already installed.

2. Open the project folder

Open the project folder in Visual Studio Code.

3. Create a virtual environment

python -m venv .venv

4. Activate the virtual environment

Windows PowerShell:

.\.venv\Scripts\Activate.ps1

5. Install dependencies

pip install -r requirements.txt

6. Run the application

python app.py

7. Open the dashboard

Open your browser and visit:

http://127.0.0.1:5000

How to Use

1. Open the dashboard in your browser.
2. Enter the required student details and add a record.
3. Search, filter, or sort student records.
4. Select Edit to update a student's information.
5. Select Delete to remove a record.
6. Review the dashboard and department statistics.
7. Select Export CSV to download the student records.

Use fictional student information when testing or demonstrating the application.

Validation Rules

- Roll numbers must be unique.
- Required fields must not be blank.
- Academic year must be between 1 and 4.
- Marks must be between 0 and 100.

Learning Outcomes

This project demonstrates basic web application development, Python programming, Flask routing, HTML templates, CSS styling, SQLite database operations, form handling, input validation, and CSV file generation.

Future Enhancements

- Login and role-based access control
- Pagination for large student lists
- Charts for academic performance
- PDF report generation
- Improved database backup and recovery

Author

Developed as a student learning and internship project.

License

This project is intended for educational purposes. Add a license file if you choose to distribute it under a specific open-source license.