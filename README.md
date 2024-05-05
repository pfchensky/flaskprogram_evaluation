# Program Evaluation System

## Overview

This Flask application is designed to facilitate the management and evaluation of academic programs. It provides tools for data entry, querying, and reporting related to degrees, courses, instructors, and evaluations.

## Features

- **Course Management**: Add, update, and delete course information.
- **Degree Management**: Manage degree details and associate courses to degrees.
- **Instructor Management**: Manage instructor profiles and their association with courses.
- **Evaluation Management**: Input and manage evaluation metrics for courses under specific degrees.
- **Data Query**: Flexible querying capabilities for courses, degrees, instructors, and evaluations.

## Installation

1. **Clone the repository:**

   ```
   git clone https://github.com/pfchensky/flaskprogram_evaluation.git
   cd flaskprogram_evaluation
   ```

2. **Setup a virtual environment:**

   ```
   python3 -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install dependencies:**

   ```
   pip install -r requirements.txt
   ```

4. **Initialize the database:**

   ```
   flask db init
   flask db migrate
   flask db upgrade
   ```

5. **Run the application:**
   ```
   flask run
   ```

## Usage

Navigate to `http://127.0.0.1:5000/` in your web browser to access the application. Use the navigation bar to access different sections of the application.

## Directory Structure

- `app.py`: The main Flask application file.
- `database.py`: Setup for the SQLAlchemy database.
- `models.py`: SQLAlchemy models for the database schema.
- `/routes`: Controllers for handling requests and responses for different parts of the application.
- `/templates`: HTML files for rendering the frontend.
- `/static`: Static files like CSS and images.

## Project Structure

```
├── README.md
├── app.py
├── database.py
├── models.py
├── requirements.txt
├── routes
│   ├── __init__.py
│   ├── __pycache__
│   ├── course_routes.py
│   ├── degree_routes.py
│   ├── evaluation_routes.py
│   ├── home_routes.py
│   ├── instructor_routes.py
│   ├── learningObject_routes.py
│   ├── query_course_routes.py
│   ├── query_degree_routes.py
│   ├── query_instructor_routes.py
│   ├── query_section_percentage_routes.py
│   ├── query_section_routes.py
│   └── section_routes.py
├── static
│   ├── background.jpg
│   └── styles.css
├── templates
│   ├── Navbar.html
│   ├── base.html
│   ├── dataEntryPage
│   ├── dataQueryPage
│   ├── evaluationPage
│   └── homepage.html
└── venv
   ├── bin
   ├── include
   ├── lib
   └── pyvenv.cfg

```
