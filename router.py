from typing import Any

from bson import ObjectId
from fastapi import APIRouter, status, Depends
from pymemcache import HashClient
from starlette.responses import Response

from cache.memcached_utils import get_memcached_client
from repository import Repository
from search_repository import SearchStudentRepository
from student import Student, UpdateStudentModel

router = APIRouter()


@router.get("/")
async def get_all_student(repository: Repository = Depends(Repository.get_instance)) -> list[Student]:
    return await repository.get_all()


@router.get("/filter")
async def get_by_name(name: str, repository: SearchStudentRepository = Depends(SearchStudentRepository.get_instance)) -> Any:
    return await repository.find_by_name(name)


@router.get("/{student_id}", response_model=Student)
async def get_by_id(student_id: str,
                    repository: Repository = Depends(Repository.get_instance),
                    memcached_client: HashClient = Depends(get_memcached_client)) -> Any:
    if not ObjectId.is_valid(student_id):
        return Response(status_code=status.HTTP_400_BAD_REQUEST)

    student = memcached_client.get(student_id)

    if student is not None:
        return student

    student = await repository.get_by_id(student_id)

    if student is None:
        return Response(status_code=status.HTTP_404_NOT_FOUND)

    memcached_client.add(student_id, student)

    return student


@router.post("/")
async def add_student(student: UpdateStudentModel,
                      repository: Repository = Depends(Repository.get_instance),
                      search_repository: SearchStudentRepository = Depends(SearchStudentRepository.get_instance)) -> str:
    student_id = await repository.create(student)
    await search_repository.create(student_id, student)
    return student_id


@router.delete("/{student_id}")
async def remove_student(student_id: str,
                         repository: Repository = Depends(Repository.get_instance),
                         search_repository: SearchStudentRepository = Depends(SearchStudentRepository.get_instance)) -> Response:
    if not ObjectId.is_valid(student_id):
        return Response(status_code=status.HTTP_400_BAD_REQUEST)
    student = await repository.delete(student_id)
    if student is None:
        return Response(status_code=status.HTTP_404_NOT_FOUND)
    await search_repository.delete(student_id)
    return Response()


@router.put("/{student_id}", response_model=Student)
async def update_student(student_id: str,
                         student_model: UpdateStudentModel,
                         repository: Repository = Depends(Repository.get_instance),
                         search_repository: SearchStudentRepository = Depends(SearchStudentRepository.get_instance)) -> Any:
    if not ObjectId.is_valid(student_id):
        return Response(status_code=status.HTTP_400_BAD_REQUEST)
    student = await repository.update(student_id, student_model)
    if student is None:
        return Response(status_code=status.HTTP_404_NOT_FOUND)
    await search_repository.update(student_id, student_model)
    return student
