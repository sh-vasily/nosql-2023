from pydantic import BaseModel


class Student(BaseModel):
    id: int
    name: str
    age: int


class UpdateStudentModel(BaseModel):
    name: str
    age: int
