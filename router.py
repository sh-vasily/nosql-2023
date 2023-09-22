from typing import Any

from fastapi import APIRouter, status
from starlette.responses import Response

from student import Student, UpdateStudentModel

router = APIRouter()

students: list[Student] = []


@router.get("/")
def get_all_student() -> list[Student]:
    return students


@router.get("/{student_id}", response_model=Student)
def get_by_id(student_id: int) -> Any:
    student = next((student for student in students if student.id == student_id), None)
    if student is None:
        return Response(status_code=status.HTTP_404_NOT_FOUND)
    return student


@router.post("/")
def add_student(student: Student) -> Student:
    students.append(student)
    return student


@router.delete("/{student_id}")
def remove_student(student_id: int) -> Response:
    student = next((student for student in students if student.id == student_id), None)
    if student is None:
        return Response(status_code=status.HTTP_404_NOT_FOUND)
    students.remove(student)
    return Response()


@router.put("/{student_id}", response_model=Student)
def update_student(student_id: int, student_model: UpdateStudentModel) -> Any:
    student = next((student for student in students if student.id == student_id), None)
    if student is None:
        return Response(status_code=status.HTTP_404_NOT_FOUND)

    student.name = student_model.name
    student.age = student_model.age

    return student
