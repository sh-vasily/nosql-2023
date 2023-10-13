from typing import Any

from bson import ObjectId

from student import Student


def map_student(student: Any) -> Student | None:
    if student is None:
        return None

    return Student(id=str(student['_id']), name=student['name'], age=student['age'])


def get_filter(id: str) -> dict:
    return {'_id': ObjectId(id)}