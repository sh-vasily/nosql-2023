from typing import Any

from bson import ObjectId
from fastapi import APIRouter, status, Depends
from motor.motor_asyncio import AsyncIOMotorCollection
from starlette.responses import Response

from db import get_db_collection
from student import Student, UpdateStudentModel

router = APIRouter()

students: list[Student] = []


def map_student(student: Any) -> Student:
    return Student(id=str(student['_id']), name=student['name'], age=student['age'])


def get_filter(id: str) -> dict:
    return {'_id': ObjectId(id)}


@router.get("/")
async def get_all_student(db_collection: AsyncIOMotorCollection = Depends(get_db_collection)) -> list[Student]:
    db_students = []
    async for student in db_collection.find():
        db_students.append(map_student(student))
    return db_students


@router.get("/{student_id}", response_model=Student)
async def get_by_id(student_id: str, db_collection: AsyncIOMotorCollection = Depends(get_db_collection)) -> Any:
    if not ObjectId.is_valid(student_id):
        return Response(status_code=status.HTTP_400_BAD_REQUEST)
    db_student = await db_collection.find_one(get_filter(student_id))
    if db_student is None:
        return Response(status_code=status.HTTP_404_NOT_FOUND)
    return map_student(db_student)


@router.post("/")
async def add_student(student: UpdateStudentModel, db_collection: AsyncIOMotorCollection = Depends(get_db_collection)) -> str:
    insert_result = await db_collection.insert_one(dict(student))
    return str(insert_result.inserted_id)


@router.delete("/{student_id}")
async def remove_student(student_id: str, db_collection: AsyncIOMotorCollection = Depends(get_db_collection)) -> Response:
    if not ObjectId.is_valid(student_id):
        return Response(status_code=status.HTTP_400_BAD_REQUEST)
    db_student = await db_collection.find_one_and_delete(get_filter(student_id))
    if db_student is None:
        return Response(status_code=status.HTTP_404_NOT_FOUND)
    return Response()


@router.put("/{student_id}", response_model=Student)
async def update_student(student_id: str, student_model: UpdateStudentModel, db_collection: AsyncIOMotorCollection = Depends(get_db_collection)) -> Any:
    if not ObjectId.is_valid(student_id):
        return Response(status_code=status.HTTP_400_BAD_REQUEST)
    student = await db_collection.find_one_and_replace(get_filter(student_id), dict(student_model))
    if student is None:
        return Response(status_code=status.HTTP_404_NOT_FOUND)
    return map_student(student)
