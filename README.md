
# Student Database CRUD API

A REST API built using Python, FastAPI, and SQLite to manage student records.

## Features

- Create student records
- Retrieve all students
- Retrieve a student by ID
- Update student details
- Delete student records
- Store records in an SQLite database

## Technologies Used

- Python
- FastAPI
- SQLite
- Uvicorn

## Setup Instructions

1. Clone or download this repository.
2. Create and activate a Python virtual environment.
3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Start the API:

   ```bash
   python -m uvicorn main:app --reload
   ```

5. Open the API documentation:

   http://127.0.0.1:8000/docs

## API Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | / | Check API status |
| POST | /students | Create a student |
| GET | /students | Retrieve all students |
| GET | /students/{student_id} | Retrieve one student |
| PUT | /students/{student_id} | Update a student |
| DELETE | /students/{student_id} | Delete a student |

## Database

The application creates an SQLite database and students table automatically when the database module initializes.

## Author

Student project — FastAPI CRUD practice.
