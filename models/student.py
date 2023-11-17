from pydantic import BaseModel


class Student(BaseModel):
    id: str
    name: str
    age: int


class UpdateStudentModel(BaseModel):
    name: str
    age: int
