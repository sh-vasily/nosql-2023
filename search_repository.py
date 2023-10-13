import os

from elasticsearch import AsyncElasticsearch
from fastapi import Depends

from elasticsearch_implementation import get_elasticsearch_client
from student import Student, UpdateStudentModel


class SearchStudentRepository:
    _elasticsearch_client: AsyncElasticsearch
    _elasticsearch_index: str

    def __init__(self, index: str, elasticsearch_client: AsyncElasticsearch):
        self._elasticsearch_client = elasticsearch_client
        self._elasticsearch_index = index

    async def create(self, student_id: str, student: UpdateStudentModel):
        await self._elasticsearch_client.create(index=self._elasticsearch_index, id=student_id, document=dict(student))

    async def update(self, student_id: str, student: UpdateStudentModel):
        await self._elasticsearch_client.update(index=self._elasticsearch_index, id=student_id, doc=dict(student))

    async def delete(self, student_id: str):
        await self._elasticsearch_client.delete(index=self._elasticsearch_index, id=student_id)

    async def find_by_name(self, name: str):
        query = {
            "match": {
                "name": {
                    "query": name
                }
            }
        }
        response = await self._elasticsearch_client.search(index=self._elasticsearch_index, query=query, filter_path=['hits.hits._id', 'hits.hits._source'])
        students = list(map(lambda student: Student(id=student['_id'], name=student['_source']['name'], age=student['_source']['age']), response.body['hits']['hits']))
        return students

    @staticmethod
    def get_instance(elasticsearch_client: AsyncElasticsearch = Depends(get_elasticsearch_client)):
        elasticsearch_index = os.getenv('ELASTICSEARCH_INDEX')
        return SearchStudentRepository(elasticsearch_index, elasticsearch_client)
