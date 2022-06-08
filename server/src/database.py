# -*- coding: utf-8 -*-

from enum import IntEnum
import sqlite3
from hmac import compare_digest
import env

class UserRole(IntEnum):
    "Represents a set of user roles."

    MANAGER = 1
    MEMBER = 2

class User:
    "The base class for the table classes."

    id = None
    name = None
    password_hash = None
    role = None
    added_at = None
    updated_at = None

class UserForm(User):
    "The form of the user table."

    def __init__(self, id, name, password_hash, role, added_at, updated_at):
        self.id = id
        self.name = name
        self.password_hash = password_hash
        self.role = role
        self.added_at = added_at
        self.updated_at = updated_at

class TaskStatus(IntEnum):
    "Represents a set of task statuses."

    OPENED = 1
    CLOSED = 2

class Task:
    "The base class for the task table."

    id = None
    description = None
    planned_at = None
    status = None
    added_at = None
    updated_at = None
    user_id = None

class TaskForm(Task):
    "The form of the task table."

    def __init__(self, id, description, planned_at, status, added_at, updated_at, user_id):
        self.id = id
        self.description = description
        self.planned_at = planned_at
        self.status = status
        self.added_at = added_at
        self.updated_at = updated_at
        self.user_id = user_id

class Gateway:
    "The base class for the query classes."

    database_uri = env.development_database_uri

    def __init__(self):
        if env.mode is env.PRODUCTION:
            self.database_uri = env.production_database_uri

class UserGateway(Gateway):
    "The class with the user queries."

    def find(self):
        "Finds rows without any conditions."
        connect = sqlite3.connect(self.database_uri)
        connect.row_factory = sqlite3.Row

        entities = []
        cursor = connect.cursor()
        cursor.execute("SELECT * FROM user;")
        for row in cursor:
            entity = UserForm(
                row['id'],
                row['name'],
                row['password_hash'],
                row['role'],
                row['added_at'],
                row['updated_at']
            )
            entities.append(entity)
        cursor.close()

        return entities

    def find_by_id(self, id):
        "Finds the row with the specific identificator."
        connect = sqlite3.connect(self.database_uri)
        connect.row_factory = sqlite3.Row

        entity = None
        cursor = connect.cursor()
        cursor.execute("SELECT * FROM user WHERE id={};".format(id))
        for row in cursor:
            entity = UserForm(
                row['id'],
                row['name'],
                row['password_hash'],
                row['role'],
                row['added_at'],
                row['updated_at']
            )
        cursor.close()

        return entity

    def find_by_name(self, name):
        "Finds the row with the specific name."
        connect = sqlite3.connect(self.database_uri)
        connect.row_factory = sqlite3.Row

        entity = None
        cursor = connect.cursor()
        cursor.execute("SELECT * FROM user WHERE name='{}';".format(name))
        for row in cursor:
            entity = UserForm(
                row['id'],
                row['name'],
                row['password_hash'],
                row['role'],
                row['added_at'],
                row['updated_at']
            )
        cursor.close()

        return entity

class TaskGateway(Gateway):
    "The class with the task queries."

    def find_by_date(self, planned_at, user_id):
        "Finds rows with the specific date."
        connect = sqlite3.connect(self.database_uri)
        connect.row_factory = sqlite3.Row

        entities = []
        cursor = connect.cursor()
        cursor.execute("SELECT * FROM task WHERE planned_at='{}' AND user_id={};".format(planned_at, user_id))
        for row in cursor:
            entity = TaskForm(
                row['id'],
                row['description'], 
                row['planned_at'],
                row['status'],
                row['added_at'],
                row['updated_at'],
                row['user_id']
            )
            entities.append(entity)
        cursor.close()

        return entities

    def create(self, description, status, planned_at, user_id):
        "Creates a row."
        connect = sqlite3.connect(self.database_uri)
        connect.row_factory = sqlite3.Row

        cursor = connect.cursor()
        cursor.execute(
            "INSERT INTO task(description, status, planned_at, user_id) values ('{}', {}, '{}', {});"
            .format(description, status, planned_at, user_id)
        )
        last_id = cursor.lastrowid
        connect.commit()
        cursor.close()

        return last_id

    def update(self, description, status, updated_at, id, user_id):
        "Updates a row."
        connect = sqlite3.connect(self.database_uri)
        connect.row_factory = sqlite3.Row

        cursor = connect.cursor()
        cursor.execute(
            "UPDATE task SET description='{}', status={}, updated_at='{}' WHERE id={} AND user_id={};"
            .format(description, status, updated_at, id, user_id)
        )
        last_id = cursor.lastrowid
        connect.commit()
        cursor.close()

        return last_id

    def delete(self, id, user_id):
        "Deletes a row."
        connect = sqlite3.connect(self.database_uri)
        connect.row_factory = sqlite3.Row

        cursor = connect.cursor()
        cursor.execute("DELETE FROM task WHERE id={} AND user_id={};".format(id, user_id))
        last_id = cursor.lastrowid
        connect.commit()
        cursor.close()

        return last_id
