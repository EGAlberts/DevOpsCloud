import json
import logging
import os
import tempfile

import pymongo
from functools import reduce
import uuid

from swagger_server.models import Student

#db_dir_path = tempfile.gettempdir()
#db_file_path = os.path.join(db_dir_path, "students.json")
client = pymongo.MongoClient("mongodb://mongodb:27017/")



student_db = client["students"]


def add_student(student):
    student_dict = student.to_dict()
    if(not student_dict["first_name"] or not student_dict["last_name"]):
        return 'invalid request, field missing (last or first name)', 405

    # queries = []
    # query = Query()
    # queries.append(query.first_name == student.first_name)
    # queries.append(query.last_name == student.last_name)
    # query = reduce(lambda a, b: a & b, queries)


    col = student_db["allstudents"]

    query = {"first_name" : student.first_name, "last_name" : student.last_name}

    res = col.find_one(query)


    
    if res:
        return 'already exists', 409

    latest_id = 0

    for doc in col.find().sort('_id', pymongo.DESCENDING):
        latest_id = int(str(doc["_id"]))
        break

    new_id = latest_id + 1
    student_dict["_id"] = new_id

    doc_id = col.insert_one(student_dict).inserted_id
    student.student_id = doc_id
    return student.student_id


def get_student_by_id(student_id, subject):
    query = {"_id" : int(student_id) }

    col = student_db["allstudents"]

    student = col.find_one(query)

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
    query = {"_id" : int(student_id) }

    col = student_db["allstudents"]
    
    student = col.find_one(query)
    
    if not student:
        return student
    student = col.delete_one(query)

    return student_id

def get_student_by_last_name(stud_last_name):
    col = student_db["allstudents"]

    query = {"last_name" : stud_last_name}

    student = col.find_one(query)

    if not student:
        return student

    student = Student.from_dict(student)

    return student
