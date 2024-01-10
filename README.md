# CRUD-Python
This project implements a simple login and registration system using Python, Django, and a MySQL database. It provides functionalities for user authentication, registration, and redirection to a dashboard displaying registered users.

## Features

- **Login:** Users can log in with their credentials.
- **Registration:** New users can sign up by providing necessary details.
- **Dashboard:** Upon successful login, users are redirected to a dashboard displaying a list of registered users.
- **List of Registered Users:** The dashboard includes a table showing all registered users.

## Setup

### Prerequisites

- Python 3.12 installed
- Using Django Framework
- MySQL database configured in localhost

### Installation

1. Clone this repository.
2. Install Django using `pip install django`.
3. Set up your MySQL database and configure the database connection in `PYTHON/settings.py` section DATABASES using the database.sql file
4. Run the application using `python manage.py runserver`.

### Usage

1. Access the application in your browser at `http://127.0.0.1:8000/`.
2. Create a new user using the registration form.
3. Upon login, you'll be redirected to the dashboard displaying registered users.

## Folder Structure

- `PYTHON/`: Project folder containing files including application routings and settings.
- `authentication/`: Application folder containing settings for the app such as views and urls.
- `templates/authentication/`: HTML template and layouting for display page.

## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvement, please open an issue or create a pull request.
