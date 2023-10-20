from fastapi import Depends
from motor.motor_asyncio import AsyncIOMotorCollection

from db import get_db_collection
from student import Student, UpdateStudentModel
from utils import map_student, get_filter


class Repository:
    _db_collection: AsyncIOMotorCollection

    def __init__(self, db_collection: AsyncIOMotorCollection):
        self._db_collection = db_collection

    async def create(self, student: UpdateStudentModel) -> str:
        insert_result = await self._db_collection.insert_one(dict(student))
        return str(insert_result.inserted_id)

    async def get_all(self) -> list[Student]:
        db_students = []
        async for student in self._db_collection.find():
            db_students.append(map_student(student))
        return db_students

    async def get_by_id(self, student_id: str) -> Student | None:
        print(f'Get student {student_id} from mongo')
        db_student = await self._db_collection.find_one(get_filter(student_id))
        return map_student(db_student)

    async def update(self, student_id: str, student: UpdateStudentModel) -> Student | None:
        db_student = await self._db_collection.find_one_and_replace(get_filter(student_id), dict(student))
        return map_student(db_student)

    async def delete(self, student_id: str) -> Student | None:
        db_student = await self._db_collection.find_one_and_delete(get_filter(student_id))
        return map_student(db_student)

    @staticmethod
    def get_instance(db_collection: AsyncIOMotorCollection = Depends(get_db_collection)):
        return Repository(db_collection)
