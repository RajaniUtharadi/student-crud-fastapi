from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr
from typing import Optional
import sqlite3

from database import get_connection

app = FastAPI(title="Student Database CRUD API")


class StudentCreate(BaseModel):
    name: str
    dob: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    course: Optional[str] = None
    address: Optional[str] = None
    enrollment_date: Optional[str] = None


@app.get("/")
def home():
    return {
        "message": "Student Database CRUD API is running",
        "docs": "/docs"
    }


@app.post("/students", status_code=201)
def create_student(student: StudentCreate):
    connection = get_connection()

    try:
        cursor = connection.execute(
            """
            INSERT INTO students
            (name, dob, email, phone, course, address, enrollment_date)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                student.name,
                student.dob,
                student.email,
                student.phone,
                student.course,
                student.address,
                student.enrollment_date,
            ),
        )

        connection.commit()
        student_id = cursor.lastrowid

        return {
            "message": "Student created successfully",
            "student_id": student_id
        }

    except sqlite3.IntegrityError:
        raise HTTPException(
            status_code=409,
            detail="This email address already exists."
        )

    finally:
        connection.close()
        
@app.get("/students")
def get_all_students():
    connection = get_connection()

    try:
        cursor = connection.execute(
            "SELECT * FROM students"
        )
        students = cursor.fetchall()

        return [dict(student) for student in students]

    finally:
        connection.close()

@app.get("/students/{student_id}")
def get_student(student_id: int):
    connection = get_connection()

    try:
        cursor = connection.execute(
            "SELECT * FROM students WHERE id = ?",
            (student_id,)
        )

        student = cursor.fetchone()

        if student is None:
            raise HTTPException(
                status_code=404,
                detail="Student not found"
            )

        return dict(student)

    finally:
        connection.close()

class StudentUpdate(BaseModel):
    name: str
    dob: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    course: Optional[str] = None
    address: Optional[str] = None
    enrollment_date: Optional[str] = None


@app.put("/students/{student_id}")
def update_student(student_id: int, student: StudentUpdate):
    connection = get_connection()

    try:
        cursor = connection.execute(
            "SELECT id FROM students WHERE id = ?",
            (student_id,)
        )

        if cursor.fetchone() is None:
            raise HTTPException(
                status_code=404,
                detail="Student not found"
            )

        connection.execute(
            """
            UPDATE students
            SET name = ?, dob = ?, email = ?, phone = ?,
                course = ?, address = ?, enrollment_date = ?
            WHERE id = ?
            """,
            (
                student.name,
                student.dob,
                student.email,
                student.phone,
                student.course,
                student.address,
                student.enrollment_date,
                student_id,
            ),
        )

        connection.commit()

        return {
            "message": "Student updated successfully",
            "student_id": student_id
        }

    except sqlite3.IntegrityError:
        raise HTTPException(
            status_code=409,
            detail="This email address already exists."
        )

    finally:
        connection.close()

@app.delete("/students/{student_id}")
def delete_student(student_id: int):
    connection = get_connection()

    try:
        cursor = connection.execute(
            "DELETE FROM students WHERE id = ?",
            (student_id,)
        )

        if cursor.rowcount == 0:
            raise HTTPException(
                status_code=404,
                detail="Student not found"
            )

        connection.commit()

        return {
            "message": "Student deleted successfully",
            "student_id": student_id
        }

    finally:
        connection.close()

