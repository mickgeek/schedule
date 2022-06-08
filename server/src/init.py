# -*- coding: utf-8 -*-

import sqlite3
import sys
import unittest
import env
from database import UserRole, TaskStatus
from utilities import UserPassword
from test_utilities import JWTEncoderTestCase, JWTDecoderTestCase, UserPasswordTestCase
from test_database import UserGatewayTestCase, TaskGatewayTestCase
from test_responses import IndexResponseTestCase, UserResponseTestCase, TaskResponseTestCase

class Initialization:
    "The console command that allows to create and drop databases, run the tests."

    user_statement="""
        CREATE TABLE user(
            id INTEGER PRIMARY KEY,
            name TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            role INTEGER NOT NULL,
            added_at TEXT NOT NULL DEFAULT(CURRENT_TIMESTAMP),
            updated_at TEXT
        );
    """
    task_statement=("""
        CREATE TABLE task(
            id INTEGER PRIMARY KEY,
            description TEXT NOT NULL,
            planned_at TEXT NOT NULL DEFAULT(CURRENT_DATE),
            status INTEGER NOT NULL DEFAULT({}),
            added_at TEXT NOT NULL DEFAULT(CURRENT_TIMESTAMP),
            updated_at TEXT,
            user_id INTEGER NOT NULL,
            FOREIGN KEY(user_id) REFERENCES user(id)
        );
    """).format(TaskStatus.OPENED)

    def create_production_database(self):
        "Creates the production database."
        connect = sqlite3.connect(env.production_database_uri)
        cursor = connect.cursor()

        cursor.execute(self.user_statement)
        cursor.execute(self.task_statement)
        cursor.execute(("""
            INSERT INTO user(name, password_hash, role)
            VALUES('michael', '{}', {});
        """).format(UserPassword().crypt_password('michael'), UserRole.MANAGER))

        connect.commit()
        connect.close()

    def delete_production_database(self):
        "Deletes the production database."
        connect = sqlite3.connect(env.production_database_uri)
        cursor = connect.cursor()
        cursor.execute("DROP TABLE task;")
        cursor.execute("DROP TABLE user;")
        connect.commit()
        connect.close()

    def create_development_database(self):
        "Creates the development database."
        connect = sqlite3.connect(env.development_database_uri)
        cursor = connect.cursor()

        cursor.execute(self.user_statement)
        cursor.execute(self.task_statement)
        cursor.execute(("""
            INSERT INTO user(id, name, password_hash, role)
            VALUES(1, 'michael', '{}', {});
        """).format(UserPassword().crypt_password('michael'), UserRole.MANAGER))
        cursor.execute(("""
            INSERT INTO user(id, name, password_hash, role)
            VALUES(2, 'emily', '{}', {});
        """).format(UserPassword().crypt_password('emily'), UserRole.MEMBER))
        cursor.execute("""
            INSERT INTO task(id, description, planned_at, user_id)
            VALUES(1, 'Edit the book of a jungle.', '2022-05-15', 1);
        """)
        cursor.execute("""
            INSERT INTO task(id, description, planned_at, user_id)
            VALUES(2, 'Delete personal files.', '2022-05-15', 1);
        """)
        cursor.execute("""
            INSERT INTO task(id, description, planned_at, user_id)
            VALUES(3, 'Clear rooms in the flat.', '2022-05-15', 2);
        """)

        connect.commit()
        connect.close()

    def delete_development_database(self):
        "Deletes the development database."
        connect = sqlite3.connect(env.development_database_uri)
        cursor = connect.cursor()
        cursor.execute("DROP TABLE task;")
        cursor.execute("DROP TABLE user;")
        connect.commit()
        connect.close()

    def run_tests(self):
        "Runs the tests."
        suite = unittest.TestSuite()
        suite.addTests([
            JWTEncoderTestCase('test_encode_header'),
            JWTEncoderTestCase('test_encode_payload'),
            JWTEncoderTestCase('test_encode_signature'),
            JWTEncoderTestCase('test_encode_token'),
            JWTDecoderTestCase('test_get_decoded_token'),
            JWTDecoderTestCase('test_get_decoded_header'),
            JWTDecoderTestCase('test_get_decoded_payload'),
            JWTDecoderTestCase('test_get_decoded_signature'),
            JWTDecoderTestCase('test_compare_signatures'),
            JWTDecoderTestCase('test_is_token_expired'),
            UserPasswordTestCase('test_crypt_password'),
            UserPasswordTestCase('test_compare_password'),
        ])
        suite.addTests([
            UserGatewayTestCase('test_find'),
            UserGatewayTestCase('test_find_by_id'),
            UserGatewayTestCase('test_find_by_name'),
            TaskGatewayTestCase('test_find_by_date'),
            TaskGatewayTestCase('test_create'),
            TaskGatewayTestCase('test_update'),
            TaskGatewayTestCase('test_delete'),
        ])
        suite.addTests([
            IndexResponseTestCase('test_authenticate'),
            IndexResponseTestCase('test_error_not_found'),
            UserResponseTestCase('test_index'),
            UserResponseTestCase('test_entity'),
            TaskResponseTestCase('test_index'),
            TaskResponseTestCase('test_entity'),
        ])
        runner = unittest.TextTestRunner()
        runner.run(suite)

if __name__ == '__main__':
    if len(sys.argv) == 1:
        print('Arguments are not found.')

    elif sys.argv[1] == 'production':
        if len(sys.argv) == 2:
            print('The second argument is not found.')
        elif sys.argv[2] == 'create':
            Initialization().create_production_database()
            print('Tables and rows were created successfully.')
        elif sys.argv[2] == 'delete':
            Initialization().delete_production_database()
            print('Tables were deleted successfully.')
    elif sys.argv[1] == 'development':
        if len(sys.argv) == 2:
            print('The second argument is not found.')
        elif sys.argv[2] == 'create':
            Initialization().create_development_database()
            print('Tables and rows were created successfully.')
        elif sys.argv[2] == 'delete':
            Initialization().delete_development_database()
            print('Tables were deleted successfully.')
    elif sys.argv[1] == 'test':
        Initialization().run_tests()
        print('Tests were runned successfully.')
    else:
        print('Arguments is not valid.')
