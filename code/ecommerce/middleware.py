import time

from rest_framework.response import Response


class MyMiddleware1:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        print('MyMiddleware1 start')
        response = self.get_response(request)
        print('MyMiddleware1 end')
        return response


class MyMiddleware2:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        print('MyMiddleware2 start')
        response = self.get_response(request)
        print('MyMiddleware2 end')
        return response
