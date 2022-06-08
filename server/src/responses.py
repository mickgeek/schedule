# -*- coding: utf-8 -*-

import ast
import time
import datetime
import re
from json import JSONEncoder
import env
from database import UserRole, UserGateway, TaskGateway
from utilities import JWTEncoder, JWTDecoder, UserPassword

SUCCESSFUL_200_STATUS = '200 OK'
SUCCESSFUL_201_STATUS = '201 Created'
ERROR_400_STATUS = '400 Bad Request'
ERROR_403_STATUS = '403 Forbidden'
ERROR_404_STATUS = '404 Not Found'
ERROR_405_STATUS = '405 Method Not Allowed'

class UserToken():
    "Validates the user token."

    token = None

    def __init__(self, token):
        self.token = token

    def is_empty(self):
        "Checks the existence."
        if self.token.token is None or self.token.token == '':
            return True

    def is_valid_signed(self, user_name, user_id, user_role):
        "Checks the token signature validation."
        header = {
            'typ': 'JWT',
            'alg': 'HS256',
        }
        payload = {
            'exp': self.token.get_decoded_payload()['exp'],
            'iss': user_name,
            'jti': user_id,
            'role': user_role,
        }
        if not self.token.compare_signatures(header, payload):
            return False

        return True

    def is_actual(self):
        "Checks the expiration time."
        if self.token.is_token_expired():
            return False

        return True

class Response():
    "Represents the response handler."

    start_response = None

    content_type = 'application/json'
    access_control_allow_headers = 'Content-Type'
    access_control_allow_methods = 'GET'
    access_control_allow_origin = env.client_endpoint

    def __init__(self, start_response):
        self.start_response = start_response

    def get_query(self, query_string):
        "Splits the query string."
        parameters = {}
        for parameter in query_string.split('&'):
            matches = re.match(r"(\w+)=(.*)", parameter)
            if matches is not None:
                parameters[matches[1]] = matches[2]
        return parameters

    def get_form(self, wsgi_input):
        "Creates the object from WSGI input data."
        return ast.literal_eval(wsgi_input.peek().decode('utf-8'))

    def create_data(self, status = SUCCESSFUL_200_STATUS, rows = [], errors = [], token = ''):
        "Creates the string with response data."
        self.start_response(status, self.get_headers())
        data = {
            'status': status,
            'rows': rows,
            'errors': errors,
            'token': token,
        }
        return JSONEncoder().encode(data).encode('utf-8')

    def get_headers(self):
        "Creates the object with response headers."
        headers = [
            ('Content-Type', self.content_type),
            ('Access-Control-Allow-Headers', self.access_control_allow_headers),
            ('Access-Control-Allow-Methods', self.access_control_allow_methods),
            ('Access-Control-Allow-Origin', self.access_control_allow_origin),
        ]
        return headers

    def set_content_type(self, content_type):
        "Set the Content-Type header."
        self.content_type = content_type

    def set_allow_headers(self, allow_headers):
        "Set the Access-Control-Allow-Headers header."
        self.access_control_allow_headers = allow_headers

    def set_allow_methods(self, allow_methods):
        "Set the Access-Control-Allow-Methods header."
        self.access_control_allow_methods = allow_methods

    def set_allow_origin(self, allow_origin):
        "Set the Access-Control-Allow-Origin header."
        self.access_control_allow_origin = allow_origin

class IndexResponse():
    "Represents the controller for the main requests."

    def authenticate(self, environ, start_response):
        "Authenticates a user with a custom expiration time."
        response = Response(start_response)
        response.set_allow_methods('OPTIONS, POST')

        if environ['REQUEST_METHOD'] == 'OPTIONS':
            data = response.create_data()
            return data

        if environ['REQUEST_METHOD'] == 'POST':
            form = response.get_form(environ['wsgi.input'])
            if (form['name'] == '' or form['password'] == ''):
                data = response.create_data(ERROR_400_STATUS)
                return data

            row = UserGateway().find_by_name(form['name'])
            if (row is None):
                data = response.create_data(SUCCESSFUL_200_STATUS, [], [{'name': 'Name is not valid.'}])
                return data
            if (UserPassword().compare_password(form['password'], row.password_hash) is False):
                data = response.create_data(SUCCESSFUL_200_STATUS, [], [{'password': 'Password is not valid.'}])
                return data

            header = {
                'typ': 'JWT',
                'alg': 'HS256',
            }
            payload = {
                'exp': round(time.time()) + env.jwt_expiration_time,
                'iss': row.name,
                'jti': row.id,
                'role': row.role,
            }
            token = JWTEncoder(header, payload).encode_token().decode('utf-8')
            data = response.create_data(SUCCESSFUL_200_STATUS, [], [], token)
            return data

        data = response.create_data(ERROR_405_STATUS)
        return data

    def error_not_found(self, environ, start_response):
        "Returns the response with 404 error."
        response = Response(start_response)
        response.set_allow_methods('OPTIONS, GET')

        if environ['REQUEST_METHOD'] == 'OPTIONS':
            data = response.create_data()
            return data

        if environ['REQUEST_METHOD'] == 'GET':
            data = response.create_data(ERROR_404_STATUS)
            return data

        data = response.create_data(ERROR_405_STATUS)
        return data

class UserResponse():
    "Represents the controller for the user requests."

    def index(self, environ, start_response):
        "Returns rows with user entities."
        response = Response(start_response)
        response.set_allow_methods('OPTIONS, GET')

        if environ['REQUEST_METHOD'] == 'OPTIONS':
            data = response.create_data()
            return data

        if environ['REQUEST_METHOD'] == 'GET':
            query = response.get_query(environ['QUERY_STRING'])
            if len(query) == 0:
                data = response.create_data(ERROR_400_STATUS)
                return data

            user_token = UserToken(JWTDecoder(query['jwt']))
            if (user_token.is_empty() is True):
                data = response.create_data(ERROR_403_STATUS, [], [{'jwt': 'Token is empty.'}])
                return data
            current_user = UserGateway().find_by_name(user_token.token.get_decoded_payload()['iss'])
            if (user_token.is_valid_signed(current_user.name, current_user.id, current_user.role) is False):
                data = response.create_data(ERROR_403_STATUS, [], [{'jwt': 'Token have not valid signature.'}])
                return data
            if (user_token.is_actual() is False):
                data = response.create_data(ERROR_403_STATUS, [], [{'jwt': 'Token is not actual.'}])
                return data
            if current_user.role not in [UserRole.MANAGER]:
                data = response.create_data(ERROR_403_STATUS, [], [{'jwt': 'Invalid access rights.'}])
                return data

            users = []
            rows = UserGateway().find()
            for row in rows:
                users.append({
                    'id': row.id,
                    'name': row.name,
                    'role': row.role,
                    'added_at': row.added_at,
                    'updated_at': row.updated_at,
                })
            data = response.create_data(SUCCESSFUL_200_STATUS, users)
            return data

        data = response.create_data(ERROR_405_STATUS)
        return data

    def entity(self, id, environ, start_response):
        "Returns rows with an entity of the specific user."
        response = Response(start_response)
        response.set_allow_methods('OPTIONS, GET')

        if environ['REQUEST_METHOD'] == 'OPTIONS':
            data = response.create_data()
            return data

        if environ['REQUEST_METHOD'] == 'GET':
            query = response.get_query(environ['QUERY_STRING'])
            if len(query) == 0:
                data = response.create_data(ERROR_400_STATUS)
                return data

            user_token = UserToken(JWTDecoder(query['jwt']))
            if (user_token.is_empty() is True):
                data = response.create_data(ERROR_403_STATUS, [], [{'jwt': 'Token is empty.'}])
                return data
            current_user = UserGateway().find_by_name(user_token.token.get_decoded_payload()['iss'])
            if (user_token.is_valid_signed(current_user.name, current_user.id, current_user.role) is False):
                data = response.create_data(ERROR_403_STATUS, [], [{'jwt': 'Token have not valid signature.'}])
                return data
            if (user_token.is_actual() is False):
                data = response.create_data(ERROR_403_STATUS, [], [{'jwt': 'Token is not actual.'}])
                return data
            if current_user.role not in [UserRole.MANAGER]:
                data = response.create_data(ERROR_403_STATUS, [], [{'jwt': 'Invalid access rights.'}])
                return data

            row = UserGateway().find_by_id(id)
            if (row is None):
                data = response.create_data(ERROR_400_STATUS)
                return data

            user = {
                'id': row.id,
                'name': row.name,
                'role': row.role,
                'added_at': row.added_at,
                'updated_at': row.updated_at,
            }
            data = response.create_data(SUCCESSFUL_200_STATUS, [user])
            return data

        data = response.create_data(ERROR_405_STATUS)
        return data

class TaskResponse():
    "Represents the controller for the task requests."

    def index(self, environ, start_response):
        "Returns rows with task entities."
        response = Response(start_response)
        response.set_allow_methods('OPTIONS, GET, PUT')

        if environ['REQUEST_METHOD'] == 'OPTIONS':
            data = response.create_data()
            return data

        if environ['REQUEST_METHOD'] == 'GET':
            query = response.get_query(environ['QUERY_STRING'])
            if len(query) == 0:
                data = response.create_data(ERROR_400_STATUS)
                return data

            user_token = UserToken(JWTDecoder(query['jwt']))
            if (user_token.is_empty() is True):
                data = response.create_data(ERROR_403_STATUS, [], [{'jwt': 'Token is empty.'}])
                return data
            current_user = UserGateway().find_by_name(user_token.token.get_decoded_payload()['iss'])
            if (user_token.is_valid_signed(current_user.name, current_user.id, current_user.role) is False):
                data = response.create_data(ERROR_403_STATUS, [], [{'jwt': 'Token have not valid signature.'}])
                return data
            if (user_token.is_actual() is False):
                data = response.create_data(ERROR_403_STATUS, [], [{'jwt': 'Token is not actual.'}])
                return data
            if current_user.role not in [UserRole.MANAGER, UserRole.MEMBER]:
                data = response.create_data(ERROR_403_STATUS, [], [{'jwt': 'Invalid access rights.'}])
                return data

            tasks = []
            rows = TaskGateway().find_by_date(query['planned_at'], current_user.id)
            for row in rows:
                tasks.append({
                    'id': row.id,
                    'description': row.description,
                    'status': row.status,
                    'planned_at': row.planned_at,
                    'added_at': row.added_at,
                    'updated_at': row.updated_at,
                    'user_id': row.user_id,
                })
            data = response.create_data(SUCCESSFUL_200_STATUS, tasks)
            return data

        if environ['REQUEST_METHOD'] == 'PUT':
            query = response.get_query(environ['QUERY_STRING'])
            if len(query) == 0:
                data = response.create_data(ERROR_400_STATUS)
                return data

            user_token = UserToken(JWTDecoder(query['jwt']))
            if (user_token.is_empty() is True):
                data = response.create_data(ERROR_403_STATUS, [], [{'jwt': 'Token is empty.'}])
                return data
            current_user = UserGateway().find_by_name(user_token.token.get_decoded_payload()['iss'])
            if (user_token.is_valid_signed(current_user.name, current_user.id, current_user.role) is False):
                data = response.create_data(ERROR_403_STATUS, [], [{'jwt': 'Token have not valid signature.'}])
                return data
            if (user_token.is_actual() is False):
                data = response.create_data(ERROR_403_STATUS, [], [{'jwt': 'Token is not actual.'}])
                return data
            if current_user.role not in [UserRole.MANAGER, UserRole.MEMBER]:
                data = response.create_data(ERROR_403_STATUS, [], [{'jwt': 'Invalid access rights.'}])
                return data

            form = response.get_form(environ['wsgi.input'])
            if (form['description'] == '' or form['status'] == 0 or form['planned_at'] == ''):
                data = response.create_data(ERROR_400_STATUS)
                return data

            task_id = TaskGateway().create(form['description'], form['status'], form['planned_at'], current_user.id)
            data = response.create_data(SUCCESSFUL_201_STATUS, [{'id': task_id}])
            return data

        data = response.create_data(ERROR_405_STATUS)
        return data

    def entity(self, id, environ, start_response):
        "Returns rows with an entity of the specific task."
        response = Response(start_response)
        response.set_allow_methods('OPTIONS, PUT, DELETE')

        if environ['REQUEST_METHOD'] == 'OPTIONS':
            data = response.create_data()
            return data

        if environ['REQUEST_METHOD'] == 'PUT':
            query = response.get_query(environ['QUERY_STRING'])
            if len(query) == 0:
                data = response.create_data(ERROR_400_STATUS)
                return data

            user_token = UserToken(JWTDecoder(query['jwt']))
            if (user_token.is_empty() is True):
                data = response.create_data(ERROR_403_STATUS, [], [{'jwt': 'Token is empty.'}])
                return data
            current_user = UserGateway().find_by_name(user_token.token.get_decoded_payload()['iss'])
            if (user_token.is_valid_signed(current_user.name, current_user.id, current_user.role) is False):
                data = response.create_data(ERROR_403_STATUS, [], [{'jwt': 'Token have not valid signature.'}])
                return data
            if (user_token.is_actual() is False):
                data = response.create_data(ERROR_403_STATUS, [], [{'jwt': 'Token is not actual.'}])
                return data
            if current_user.role not in [UserRole.MANAGER, UserRole.MEMBER]:
                data = response.create_data(ERROR_403_STATUS, [], [{'jwt': 'Invalid access rights.'}])
                return data

            form = response.get_form(environ['wsgi.input'])
            if (form['description'] == '' or form['status'] == 0):
                data = response.create_data(ERROR_400_STATUS)
                return data

            updated_at = datetime.datetime.now().isoformat(' ', 'seconds')
            TaskGateway().update(form['description'], form['status'], updated_at, id, current_user.id)
            data = response.create_data(SUCCESSFUL_200_STATUS)
            return data

        if environ['REQUEST_METHOD'] == 'DELETE':
            query = response.get_query(environ['QUERY_STRING'])
            if len(query) == 0:
                data = response.create_data(ERROR_400_STATUS)
                return data

            user_token = UserToken(JWTDecoder(query['jwt']))
            if (user_token.is_empty() is True):
                data = response.create_data(ERROR_403_STATUS, [], [{'jwt': 'Token is empty.'}])
                return data
            current_user = UserGateway().find_by_name(user_token.token.get_decoded_payload()['iss'])
            if (user_token.is_valid_signed(current_user.name, current_user.id, current_user.role) is False):
                data = response.create_data(ERROR_403_STATUS, [], [{'jwt': 'Token have not valid signature.'}])
                return data
            if (user_token.is_actual() is False):
                data = response.create_data(ERROR_403_STATUS, [], [{'jwt': 'Token is not actual.'}])
                return data
            if current_user.role not in [UserRole.MANAGER, UserRole.MEMBER]:
                data = response.create_data(ERROR_403_STATUS, [], [{'jwt': 'Invalid access rights.'}])
                return data

            TaskGateway().delete(id, current_user.id)
            data = response.create_data(SUCCESSFUL_200_STATUS)
            return data

        data = response.create_data(ERROR_405_STATUS)
        return data
