import os
import random
import uuid

import requests

from dotenv import load_dotenv

load_dotenv('tests.env')

API_URL = os.getenv('API_URL')


def create_student(name=None, age=None):
    if name is None:
        name = str(uuid.uuid4())
    if age is None:
        age = random.randint(17, 25)
    response = requests.post(API_URL, json={
        'name': name,
        'age': age,
    })
    return response.json()


def test_student_creation():
    name = str(uuid.uuid4())
    age = random.randint(17, 25)
    created_student_id = create_student(name, age)
    student_url = f'{API_URL}/{created_student_id}'
    student = requests.get(student_url).json()
    assert student['name'] == name
    assert student['age'] == age
    requests.delete(student_url)


def test_search_student_by_name():
    name = str(uuid.uuid4())
    age = random.randint(17, 25)
    created_ids = [create_student(name, age), create_student(), create_student()]
    students = requests.get(f'{API_URL}/filter?name={name}').json()
    assert len(students) == 1
    assert students[0]['name'] == name
    assert students[0]['age'] == age
    for created_id in created_ids:
        requests.delete(f'{API_URL}/{created_id}')
