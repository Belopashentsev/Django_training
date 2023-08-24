from django.http import HttpRequest
import time


def set_useragent_on_request_middleweare(get_response):
    print("initial call")
    def mddleweare(request: HttpRequest):
        print("before get response")
        request.user_agent = request.META["HTTP_USER_AGENT"]
        response = get_response(request)
        print("after get response")
        return response

    return mddleweare


class CountResponseMiddleweare:
    def __init__(self, get_response):
        print('init____', get_response)
        self.get_response = get_response
        self.requests_count = 0
        self.responses_count = 0
        self.exceptions_count = 0

    def __call__(self, request: HttpRequest):
        self.requests_count += 1
        print('Requests count', self.requests_count)
        response = self.get_response(request)
        self.responses_count += 1
        print('Responses count', self.responses_count)
        return response

    def process_exception(self, request: HttpRequest, exception: Exception):
        self.exceptions_count += 1
        print('Got', self.exceptions_count, 'exceptions so far.')


class ThrotlingMiddleweare:
    def __init__(self, get_response):
        self.get_response = get_response
        self.IP_DICT = {}

    def __call__(self, request: HttpRequest ):
        IP_of_req = request.META['REMOTE_ADDR']
        if IP_of_req in self.IP_DICT and time.time() - self.IP_DICT[IP_of_req] < 10:
            raise Exception('Less than 10 seconds have passed since the previous request.')
        else:
            self.IP_DICT[IP_of_req] = time.time()
            return self.get_response(request)





