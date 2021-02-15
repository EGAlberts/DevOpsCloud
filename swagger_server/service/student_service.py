import json
import logging
import os
import tempfile

from tinydb import TinyDB, Query, where
from tinydb.middlewares import CachingMiddleware
from functools import reduce
import uuid

from swagger_server.models import Student

db_dir_path = tempfile.gettempdir()
db_file_path = os.path.join(db_dir_path, "students.json")
student_db = TinyDB(db_file_path)


def add_student(student):
    student_dict = student.to_dict()
    if(not student_dict["first_name"] or not student_dict["last_name"]):
        return 'invalid request, field missing (last or first name)', 405

    queries = []
    query = Query()
    queries.append(query.first_name == student.first_name)
    queries.append(query.last_name == student.last_name)
    query = reduce(lambda a, b: a & b, queries)
    res = student_db.search(query)
    if res:
        return 'already exists', 409

    doc_id = student_db.insert(student_dict)
    student.student_id = doc_id
    return student.student_id


def get_student_by_id(student_id, subject):
    student = student_db.get(doc_id=int(student_id))
    if not student:
        return student
    
    student = Student.from_dict(student)
    if not subject:
        return student
    grades = student.grades
    if subject in grades:
        return student
    else: 
        return 'could not find student with this subject', 404
    


def delete_student(student_id):
    student = student_db.get(doc_id=int(student_id))
    if not student:
        return student
    student_db.remove(doc_ids=[int(student_id)])
    return student_id

def get_student_by_last_name(stud_last_name):
    student = student_db.search(where('last_name') == stud_last_name)[0] #just going to take the first one that is found
    if not student:
        return student
    student = Student.from_dict(student)
    print(student)
    return student
