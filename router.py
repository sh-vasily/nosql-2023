from typing import Any

from bson import ObjectId
from fastapi import APIRouter, status, Depends
from starlette.responses import Response

from repository import Repository
from student import Student, UpdateStudentModel

router = APIRouter()


@router.get("/")
async def get_all_student(repository: Repository = Depends(Repository.get_instance)) -> list[Student]:
    return await repository.get_all()


@router.get("/{student_id}", response_model=Student)
async def get_by_id(student_id: str,
                    repository: Repository = Depends(Repository.get_instance)) -> Any:
    if not ObjectId.is_valid(student_id):
        return Response(status_code=status.HTTP_400_BAD_REQUEST)
    student = await repository.get_by_id(student_id)
    if student is None:
        return Response(status_code=status.HTTP_404_NOT_FOUND)
    return student


@router.post("/")
async def add_student(student: UpdateStudentModel,
                      repository: Repository = Depends(Repository.get_instance)) -> str:
    return await repository.create(student)


@router.delete("/{student_id}")
async def remove_student(student_id: str,
                         repository: Repository = Depends(Repository.get_instance)) -> Response:
    if not ObjectId.is_valid(student_id):
        return Response(status_code=status.HTTP_400_BAD_REQUEST)
    student = await repository.delete(student_id)
    if student is None:
        return Response(status_code=status.HTTP_404_NOT_FOUND)
    return Response()


@router.put("/{student_id}", response_model=Student)
async def update_student(student_id: str,
                         student_model: UpdateStudentModel,
                         repository: Repository = Depends(Repository.get_instance)) -> Any:
    if not ObjectId.is_valid(student_id):
        return Response(status_code=status.HTTP_400_BAD_REQUEST)
    student = await repository.update(student_id, student_model)
    if student is None:
        return Response(status_code=status.HTTP_404_NOT_FOUND)
    return student
