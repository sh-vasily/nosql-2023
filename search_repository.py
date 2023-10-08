from elasticsearch import AsyncElasticsearch
from fastapi import Depends

from elasticsearch_implementation import get_elasticsearch_client
from student import Student, UpdateStudentModel


class SearchStudentRepository:
    _elasticsearch_client: AsyncElasticsearch

    def __init__(self, elasticsearch_client: AsyncElasticsearch):
        self._elasticsearch_client = elasticsearch_client

    async def create(self, student_id: str, student: UpdateStudentModel):
        await self._elasticsearch_client.create(index='students', id=student_id, document=dict(student))

    async def update(self, student: Student):
        pass

    async def delete(self, student_id: str):
        await self._elasticsearch_client.delete(index='students', id=student_id)

    async def find_by_name(self, name: str):
        query = {
            "match": {
                "name": {
                    "query": name
                }
            }
        }
        response = await self._elasticsearch_client.search(index='students', query=query)
        students = list(map(lambda student: Student(id=student['_id'], name=student['_source']['name'], age=student['_source']['age']), response.body['hits']['hits']))
        return students

    @staticmethod
    def get_instance(elasticsearch_client: AsyncElasticsearch = Depends(get_elasticsearch_client)):
        return SearchStudentRepository(elasticsearch_client)
