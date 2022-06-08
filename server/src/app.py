# -*- coding: utf-8 -*-

import re
from wsgiref.simple_server import make_server
from responses import IndexResponse, UserResponse, TaskResponse

class Application():
    "Represents the class that starts the WSGI application."

    def __call__(self, environ, start_response):
        return self.handle_response(environ, start_response)

    def handle_response(self, environ, start_response):
        "Handles the response."
        path = environ.get('PATH_INFO')
        matches = re.match(r"/(\w+)/(\d+)", path)

        if path == '/authenticate':
            response = IndexResponse().authenticate(environ, start_response)
            return [response]
        elif path == '/users':
            response = UserResponse().index(environ, start_response)
            return [response]
        elif path == '/tasks':
            response = TaskResponse().index(environ, start_response)
            return [response]
        elif matches is not None:
            if matches[1] == 'users':
                response = UserResponse().entity(matches[2], environ, start_response)
                return [response]
            elif matches[1] == 'tasks':
                response = TaskResponse().entity(matches[2], environ, start_response)
                return [response]

        response = IndexResponse().error_not_found(environ, start_response)
        return [response]

if __name__ == '__main__':
    app = Application()
    make_server('0.0.0.0', 5000, app).serve_forever()
