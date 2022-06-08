import ast
import unittest
from unittest.mock import patch
from responses import IndexResponse, UserResponse, TaskResponse
from database import TaskStatus

#header = {'typ': 'JWT', 'alg': 'HS256'}
#payload = {'exp': 5000000000, 'iss': 'michael', 'jti': 1, 'role': 1}
manager_jwt = 'WzEyMywgMzksIDExNiwgMTIxLCAxMTIsIDM5LCA1OCwgMzIsIDM5LCA3NCwgODcsIDg0LCAzOSwgNDQsIDMyLCAzOSwgOTcsIDEwOCwgMTAzLCAzOSwgNTgsIDMyLCAzOSwgNzIsIDgzLCA1MCwgNTMsIDU0LCAzOSwgMTI1XQ==.WzEyMywgMzksIDEwMSwgMTIwLCAxMTIsIDM5LCA1OCwgMzIsIDUzLCA0OCwgNDgsIDQ4LCA0OCwgNDgsIDQ4LCA0OCwgNDgsIDQ4LCA0NCwgMzIsIDM5LCAxMDUsIDExNSwgMTE1LCAzOSwgNTgsIDMyLCAzOSwgMTA5LCAxMDUsIDk5LCAxMDQsIDk3LCAxMDEsIDEwOCwgMzksIDQ0LCAzMiwgMzksIDEwNiwgMTE2LCAxMDUsIDM5LCA1OCwgMzIsIDQ5LCA0NCwgMzIsIDM5LCAxMTQsIDExMSwgMTA4LCAxMDEsIDM5LCA1OCwgMzIsIDQ5LCAxMjVd.w9po9v1t9k6-2mOFSwlVVQbt4AZF32vdyoKQwEen8D4='

#header = {'typ': 'JWT', 'alg': 'HS256'}
#payload = {'exp': 5000000000, 'iss': 'michael', 'jti': 0, 'role': 0}
invalid_signed_jwt = 'WzEyMywgMzksIDExNiwgMTIxLCAxMTIsIDM5LCA1OCwgMzIsIDM5LCA3NCwgODcsIDg0LCAzOSwgNDQsIDMyLCAzOSwgOTcsIDEwOCwgMTAzLCAzOSwgNTgsIDMyLCAzOSwgNzIsIDgzLCA1MCwgNTMsIDU0LCAzOSwgMTI1XQ==.WzEyMywgMzksIDEwMSwgMTIwLCAxMTIsIDM5LCA1OCwgMzIsIDUzLCA0OCwgNDgsIDQ4LCA0OCwgNDgsIDQ4LCA0OCwgNDgsIDQ4LCA0NCwgMzIsIDM5LCAxMDUsIDExNSwgMTE1LCAzOSwgNTgsIDMyLCAzOSwgMTA5LCAxMDUsIDk5LCAxMDQsIDk3LCAxMDEsIDEwOCwgMzksIDQ0LCAzMiwgMzksIDEwNiwgMTE2LCAxMDUsIDM5LCA1OCwgMzIsIDQ4LCA0NCwgMzIsIDM5LCAxMTQsIDExMSwgMTA4LCAxMDEsIDM5LCA1OCwgMzIsIDQ4LCAxMjVd.3BCaOrTaSI9T9xNOCiReWgYGu67EvJW1vrLEMOhx03M='

#header = {'typ': 'JWT', 'alg': 'HS256'}
#payload = {'exp': 1500000000, 'iss': 'michael', 'jti': 1, 'role': 1}
not_actual_jwt = 'WzEyMywgMzksIDExNiwgMTIxLCAxMTIsIDM5LCA1OCwgMzIsIDM5LCA3NCwgODcsIDg0LCAzOSwgNDQsIDMyLCAzOSwgOTcsIDEwOCwgMTAzLCAzOSwgNTgsIDMyLCAzOSwgNzIsIDgzLCA1MCwgNTMsIDU0LCAzOSwgMTI1XQ==.WzEyMywgMzksIDEwMSwgMTIwLCAxMTIsIDM5LCA1OCwgMzIsIDQ5LCA1MywgNDgsIDQ4LCA0OCwgNDgsIDQ4LCA0OCwgNDgsIDQ4LCA0NCwgMzIsIDM5LCAxMDUsIDExNSwgMTE1LCAzOSwgNTgsIDMyLCAzOSwgMTA5LCAxMDUsIDk5LCAxMDQsIDk3LCAxMDEsIDEwOCwgMzksIDQ0LCAzMiwgMzksIDEwNiwgMTE2LCAxMDUsIDM5LCA1OCwgMzIsIDQ5LCA0NCwgMzIsIDM5LCAxMTQsIDExMSwgMTA4LCAxMDEsIDM5LCA1OCwgMzIsIDQ5LCAxMjVd.CsIU1xc7oV_K1Ey8k9Lw5Xelc0IDi7nmPqqFsTe9BqA='

#header = {'typ': 'JWT', 'alg': 'HS256'}
#payload = {'exp': 5000000000, 'iss': 'emily', 'jti': 2, 'role': 2}
member_jwt = 'WzEyMywgMzksIDExNiwgMTIxLCAxMTIsIDM5LCA1OCwgMzIsIDM5LCA3NCwgODcsIDg0LCAzOSwgNDQsIDMyLCAzOSwgOTcsIDEwOCwgMTAzLCAzOSwgNTgsIDMyLCAzOSwgNzIsIDgzLCA1MCwgNTMsIDU0LCAzOSwgMTI1XQ==.WzEyMywgMzksIDEwMSwgMTIwLCAxMTIsIDM5LCA1OCwgMzIsIDUzLCA0OCwgNDgsIDQ4LCA0OCwgNDgsIDQ4LCA0OCwgNDgsIDQ4LCA0NCwgMzIsIDM5LCAxMDUsIDExNSwgMTE1LCAzOSwgNTgsIDMyLCAzOSwgMTAxLCAxMDksIDEwNSwgMTA4LCAxMjEsIDM5LCA0NCwgMzIsIDM5LCAxMDYsIDExNiwgMTA1LCAzOSwgNTgsIDMyLCA1MCwgNDQsIDMyLCAzOSwgMTE0LCAxMTEsIDEwOCwgMTAxLCAzOSwgNTgsIDMyLCA1MCwgMTI1XQ==.g3SyBMB07HcwUrPYFDFkCQvz0PfodT6kl3Ilp_zGppU='

def start_response(status, response_headers, exc_info=None):
    if exc_info:
        try:
            pass
        finally:
            exc_info = None

class ResponseFormMock:

    def get_form(self, wsgi_input):
        """Lorem ipsum dolor sit amet..."""
        return ast.literal_eval(wsgi_input.decode('utf-8'))

    def __call__(self, *args):
        return self.get_form(*args)

class ResponseDataMock:

    def create_data(self, status = '200 OK', rows = [], errors = [], token = ''):
        data = {
            'status': status,
            'rows': rows,
            'errors': errors,
            'token': token,
        }
        return data

    def __call__(self, *args):
        return self.create_data(*args)

class IndexResponseTestCase(unittest.TestCase):

    @patch('responses.Response.get_form', new_callable=ResponseFormMock)
    @patch('responses.Response.create_data', new_callable=ResponseDataMock)
    def test_authenticate(self, get_form, create_data):
        environ = {
            'REQUEST_METHOD': 'OPTIONS',
        }
        response = IndexResponse().authenticate(environ, start_response)
        self.assertEqual(response['status'], '200 OK')

        environ = {
            'REQUEST_METHOD': 'HEAD',
        }
        response = IndexResponse().authenticate(environ, start_response)
        self.assertEqual(response['status'], '405 Method Not Allowed')

        # POST-request
        body = {
            'name': '',
            'password': '',
        }
        environ = {
            'REQUEST_METHOD': 'POST',
            'wsgi.input': str(body).encode('utf-8'),
        }
        response = IndexResponse().authenticate(environ, start_response)
        self.assertEqual(response['status'], '400 Bad Request')

        body = {
            'name': 'm',
            'password': 'michael',
        }
        environ = {
            'REQUEST_METHOD': 'POST',
            'wsgi.input': str(body).encode('utf-8'),
        }
        response = IndexResponse().authenticate(environ, start_response)
        self.assertEqual(response['status'], '200 OK')
        self.assertIn('name', response['errors'][0])

        body = {
            'name': 'michael',
            'password': 'm',
        }
        environ = {
            'REQUEST_METHOD': 'POST',
            'wsgi.input': str(body).encode('utf-8'),
        }
        response = IndexResponse().authenticate(environ, start_response)
        self.assertEqual(response['status'], '200 OK')
        self.assertIn('password', response['errors'][0])

        body = {
            'name': 'michael',
            'password': 'michael',
        }
        environ = {
            'REQUEST_METHOD': 'POST',
            'wsgi.input': str(body).encode('utf-8'),
        }
        response = IndexResponse().authenticate(environ, start_response)
        self.assertEqual(response['status'], '200 OK')

    @patch('responses.Response.create_data', new_callable=ResponseDataMock)
    def test_error_not_found(self, create_data):
        environ = {
            'REQUEST_METHOD': 'OPTIONS',
        }
        response = IndexResponse().authenticate(environ, start_response)
        self.assertEqual(response['status'], '200 OK')

        environ = {
            'REQUEST_METHOD': 'HEAD',
        }
        response = IndexResponse().error_not_found(environ, start_response)
        self.assertEqual(response['status'], '405 Method Not Allowed')

        # GET-request
        environ = {
            'REQUEST_METHOD': 'GET',
        }
        response = IndexResponse().error_not_found(environ, start_response)
        self.assertEqual(response['status'], '404 Not Found')

class UserResponseTestCase(unittest.TestCase):

    @patch('responses.Response.get_form', new_callable=ResponseFormMock)
    @patch('responses.Response.create_data', new_callable=ResponseDataMock)
    def test_index(self, get_form, create_data):
        environ = {
            'REQUEST_METHOD': 'OPTIONS',
        }
        response = UserResponse().index(environ, start_response)
        self.assertEqual(response['status'], '200 OK')

        environ = {
            'REQUEST_METHOD': 'HEAD',
        }
        response = UserResponse().index(environ, start_response)
        self.assertEqual(response['status'], '405 Method Not Allowed')

        # GET-request
        environ = {
            'REQUEST_METHOD': 'GET',
            'QUERY_STRING': '',
        }
        response = UserResponse().index(environ, start_response)
        self.assertEqual(response['status'], '400 Bad Request')

        environ = {
            'REQUEST_METHOD': 'GET',
            'QUERY_STRING': 'jwt=',
        }
        response = UserResponse().index(environ, start_response)
        self.assertEqual(response['status'], '403 Forbidden')

        environ = {
            'REQUEST_METHOD': 'GET',
            'QUERY_STRING': 'jwt={}'.format(invalid_signed_jwt),
        }
        response = UserResponse().index(environ, start_response)
        self.assertEqual(response['status'], '403 Forbidden')

        environ = {
            'REQUEST_METHOD': 'GET',
            'QUERY_STRING': 'jwt={}'.format(not_actual_jwt),
        }
        response = UserResponse().index(environ, start_response)
        self.assertEqual(response['status'], '403 Forbidden')

        environ = {
            'REQUEST_METHOD': 'GET',
            'QUERY_STRING': 'jwt={}'.format(manager_jwt),
        }
        response = UserResponse().index(environ, start_response)
        self.assertEqual(response['status'], '200 OK')

        environ = {
            'REQUEST_METHOD': 'GET',
            'QUERY_STRING': 'jwt={}'.format(member_jwt),
        }
        response = UserResponse().index(environ, start_response)
        self.assertEqual(response['status'], '403 Forbidden')

    @patch('responses.Response.create_data', new_callable=ResponseDataMock)
    def test_entity(self, create_data):
        environ = {
            'REQUEST_METHOD': 'OPTIONS',
        }
        response = UserResponse().entity(2, environ, start_response)
        self.assertEqual(response['status'], '200 OK')

        environ = {
            'REQUEST_METHOD': 'HEAD',
        }
        response = UserResponse().entity(2, environ, start_response)
        self.assertEqual(response['status'], '405 Method Not Allowed')

        # GET-request
        environ = {
            'REQUEST_METHOD': 'GET',
            'QUERY_STRING': '',
        }
        response = UserResponse().entity(2, environ, start_response)
        self.assertEqual(response['status'], '400 Bad Request')

        environ = {
            'REQUEST_METHOD': 'GET',
            'QUERY_STRING': 'jwt=',
        }
        response = UserResponse().entity(2, environ, start_response)
        self.assertEqual(response['status'], '403 Forbidden')

        environ = {
            'REQUEST_METHOD': 'GET',
            'QUERY_STRING': 'jwt={}'.format(invalid_signed_jwt),
        }
        response = UserResponse().entity(2, environ, start_response)
        self.assertEqual(response['status'], '403 Forbidden')

        environ = {
            'REQUEST_METHOD': 'GET',
            'QUERY_STRING': 'jwt={}'.format(not_actual_jwt),
        }
        response = UserResponse().entity(2, environ, start_response)
        self.assertEqual(response['status'], '403 Forbidden')

        environ = {
            'REQUEST_METHOD': 'GET',
            'QUERY_STRING': 'jwt={}'.format(member_jwt),
        }
        response = UserResponse().entity(2, environ, start_response)
        self.assertEqual(response['status'], '403 Forbidden')

        environ = {
            'REQUEST_METHOD': 'GET',
            'QUERY_STRING': 'jwt={}'.format(manager_jwt),
        }
        response = UserResponse().entity(2, environ, start_response)
        self.assertEqual(response['status'], '200 OK')

        environ = {
            'REQUEST_METHOD': 'GET',
            'QUERY_STRING': 'jwt={}'.format(manager_jwt),
        }
        response = UserResponse().entity(0, environ, start_response)
        self.assertEqual(response['status'], '400 Bad Request')

        environ = {
            'REQUEST_METHOD': 'GET',
            'QUERY_STRING': 'jwt={}'.format(manager_jwt),
        }
        response = UserResponse().entity(2, environ, start_response)
        self.assertEqual(response['rows'][0]['name'], 'emily')
        self.assertEqual(response['status'], '200 OK')

class TaskResponseTestCase(unittest.TestCase):

    @patch('responses.Response.get_form', new_callable=ResponseFormMock)
    @patch('responses.Response.create_data', new_callable=ResponseDataMock)
    def test_index(self, get_form, create_data):
        environ = {
            'REQUEST_METHOD': 'OPTIONS',
        }
        response = TaskResponse().index(environ, start_response)
        self.assertEqual(response['status'], '200 OK')

        environ = {
            'REQUEST_METHOD': 'HEAD',
        }
        response = TaskResponse().index(environ, start_response)
        self.assertEqual(response['status'], '405 Method Not Allowed')

        # GET-request
        environ = {
            'REQUEST_METHOD': 'GET',
            'QUERY_STRING': '',
        }
        response = TaskResponse().index(environ, start_response)
        self.assertEqual(response['status'], '400 Bad Request')

        environ = {
            'REQUEST_METHOD': 'GET',
            'QUERY_STRING': 'jwt=',
        }
        response = TaskResponse().index(environ, start_response)
        self.assertEqual(response['status'], '403 Forbidden')

        environ = {
            'REQUEST_METHOD': 'GET',
            'QUERY_STRING': 'jwt={}'.format(invalid_signed_jwt),
        }
        response = TaskResponse().index(environ, start_response)
        self.assertEqual(response['status'], '403 Forbidden')

        environ = {
            'REQUEST_METHOD': 'GET',
            'QUERY_STRING': 'jwt={}'.format(not_actual_jwt),
        }
        response = TaskResponse().index(environ, start_response)
        self.assertEqual(response['status'], '403 Forbidden')

        environ = {
            'REQUEST_METHOD': 'GET',
            'QUERY_STRING': 'jwt={}&planned_at=2022-05-15'.format(manager_jwt),
        }
        response = TaskResponse().index(environ, start_response)
        self.assertEqual(response['rows'][0]['id'], 1)
        self.assertEqual(response['rows'][1]['id'], 2)
        self.assertEqual(response['status'], '200 OK')

        environ = {
            'REQUEST_METHOD': 'GET',
            'QUERY_STRING': 'jwt={}&planned_at=2022-05-15'.format(member_jwt),
        }
        response = TaskResponse().index(environ, start_response)
        self.assertEqual(response['rows'][0]['id'], 3)
        self.assertEqual(response['status'], '200 OK')

        # PUT-request
        environ = {
            'REQUEST_METHOD': 'PUT',
            'QUERY_STRING': '',
        }
        response = TaskResponse().index(environ, start_response)
        self.assertEqual(response['status'], '400 Bad Request')

        environ = {
            'REQUEST_METHOD': 'PUT',
            'QUERY_STRING': 'jwt=',
        }
        response = TaskResponse().index(environ, start_response)
        self.assertEqual(response['status'], '403 Forbidden')

        environ = {
            'REQUEST_METHOD': 'PUT',
            'QUERY_STRING': 'jwt={}'.format(invalid_signed_jwt),
        }
        response = TaskResponse().index(environ, start_response)
        self.assertEqual(response['status'], '403 Forbidden')

        environ = {
            'REQUEST_METHOD': 'PUT',
            'QUERY_STRING': 'jwt={}'.format(not_actual_jwt),
        }
        response = TaskResponse().index(environ, start_response)
        self.assertEqual(response['status'], '403 Forbidden')

        body = {
            'description': '',
            'status': 0,
            'planned_at': '',
        }
        environ = {
            'REQUEST_METHOD': 'PUT',
            'QUERY_STRING': 'jwt={}'.format(manager_jwt),
            'wsgi.input': str(body).encode('utf-8'),
        }
        response = TaskResponse().index(environ, start_response)
        self.assertEqual(response['status'], '400 Bad Request')

        body = {
            'planned_at': '2022-05-15',
            'description': 'Generate a random hash with a salt.',
            'status': TaskStatus.OPENED.value,
        }
        environ = {
            'REQUEST_METHOD': 'PUT',
            'QUERY_STRING': 'jwt={}'.format(manager_jwt),
            'wsgi.input': str(body).encode('utf-8'),
        }
        response = TaskResponse().index(environ, start_response)
        self.assertEqual(response['status'], '201 Created')

        body = {
            'planned_at': '2022-05-15',
            'description': 'Write a new chapter about friends.',
            'status': TaskStatus.OPENED.value,
        }
        environ = {
            'REQUEST_METHOD': 'PUT',
            'QUERY_STRING': 'jwt={}'.format(member_jwt),
            'wsgi.input': str(body).encode('utf-8'),
        }
        response = TaskResponse().index(environ, start_response)
        self.assertEqual(response['status'], '201 Created')

    @patch('responses.Response.get_form', new_callable=ResponseFormMock)
    @patch('responses.Response.create_data', new_callable=ResponseDataMock)
    def test_entity(self, get_form, create_data):
        environ = {
            'REQUEST_METHOD': 'OPTIONS',
        }
        response = TaskResponse().entity(1, environ, start_response)
        self.assertEqual(response['status'], '200 OK')

        environ = {
            'REQUEST_METHOD': 'HEAD',
        }
        response = TaskResponse().entity(1, environ, start_response)
        self.assertEqual(response['status'], '405 Method Not Allowed')

        # PUT-request
        environ = {
            'REQUEST_METHOD': 'PUT',
            'QUERY_STRING': '',
        }
        response = TaskResponse().entity(1, environ, start_response)
        self.assertEqual(response['status'], '400 Bad Request')

        environ = {
            'REQUEST_METHOD': 'PUT',
            'QUERY_STRING': 'jwt=',
        }
        response = TaskResponse().entity(1, environ, start_response)
        self.assertEqual(response['status'], '403 Forbidden')

        environ = {
            'REQUEST_METHOD': 'PUT',
            'QUERY_STRING': 'jwt={}'.format(invalid_signed_jwt),
        }
        response = TaskResponse().entity(1, environ, start_response)
        self.assertEqual(response['status'], '403 Forbidden')

        environ = {
            'REQUEST_METHOD': 'PUT',
            'QUERY_STRING': 'jwt={}'.format(not_actual_jwt),
        }
        response = TaskResponse().entity(1, environ, start_response)
        self.assertEqual(response['status'], '403 Forbidden')

        body = {
            'description': '',
            'status': 0,
        }
        environ = {
            'REQUEST_METHOD': 'PUT',
            'QUERY_STRING': 'jwt={}'.format(manager_jwt),
            'wsgi.input': str(body).encode('utf-8'),
        }
        response = TaskResponse().entity(4, environ, start_response)
        self.assertEqual(response['status'], '400 Bad Request')

        body = {
            'id': 4,
            'description': 'Update three function.',
            'status': TaskStatus.CLOSED.value,
        }
        environ = {
            'REQUEST_METHOD': 'PUT',
            'QUERY_STRING': 'jwt={}'.format(manager_jwt),
            'wsgi.input': str(body).encode('utf-8'),
        }
        response = TaskResponse().entity(4, environ, start_response)
        self.assertEqual(response['status'], '200 OK')

        body = {
            'id': 5,
            'description': 'Edit last pages.',
            'status': TaskStatus.CLOSED.value,
        }
        environ = {
            'REQUEST_METHOD': 'PUT',
            'QUERY_STRING': 'jwt={}'.format(member_jwt),
            'wsgi.input': str(body).encode('utf-8'),
        }
        response = TaskResponse().entity(5, environ, start_response)
        self.assertEqual(response['status'], '200 OK')

        # DELETE-request
        environ = {
            'REQUEST_METHOD': 'DELETE',
            'QUERY_STRING': '',
        }
        response = TaskResponse().entity(1, environ, start_response)
        self.assertEqual(response['status'], '400 Bad Request')

        environ = {
            'REQUEST_METHOD': 'DELETE',
            'QUERY_STRING': 'jwt=',
        }
        response = TaskResponse().entity(1, environ, start_response)
        self.assertEqual(response['status'], '403 Forbidden')

        environ = {
            'REQUEST_METHOD': 'DELETE',
            'QUERY_STRING': 'jwt={}'.format(invalid_signed_jwt),
        }
        response = TaskResponse().entity(1, environ, start_response)
        self.assertEqual(response['status'], '403 Forbidden')

        environ = {
            'REQUEST_METHOD': 'DELETE',
            'QUERY_STRING': 'jwt={}'.format(not_actual_jwt),
        }
        response = TaskResponse().entity(1, environ, start_response)
        self.assertEqual(response['status'], '403 Forbidden')

        environ = {
            'REQUEST_METHOD': 'DELETE',
            'QUERY_STRING': 'jwt={}'.format(manager_jwt),
        }
        response = TaskResponse().entity(4, environ, start_response)
        self.assertEqual(response['status'], '200 OK')

        environ = {
            'REQUEST_METHOD': 'DELETE',
            'QUERY_STRING': 'jwt={}'.format(member_jwt),
        }
        response = TaskResponse().entity(5, environ, start_response)
        self.assertEqual(response['status'], '200 OK')
