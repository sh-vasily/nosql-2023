from flask import request, jsonify
import json
import uuid

from student import Student

students = []


def hello_world():
    return "<h1>Hello, world</h1>"


def get_all_students():
    return jsonify(list(students))


def save():
    try:
        name, age = request.json['name'], request.json['age']
    except:
        return {"Error": "Some error during reading request"}

    id = uuid.uuid4()
    students.append(Student(id, name, age))
    return {"id": id}, 201
