import requests


class HttpClient:

    AUTH_TOKEN_HEADER_IDENTIFIER = 'x-gl-token-external'

    def __init__(self, base_url, request_uri):
        self.BASE_URL = base_url
        self.REQUEST_URI = request_uri

    def initiate_request(self, gl_merchant_request):

        final_url = self.BASE_URL + self.REQUEST_URI
        headers = {
            self.AUTH_TOKEN_HEADER_IDENTIFIER: gl_merchant_request.get_xgl_token_external(),
            'Content-Type': 'text/plain'
        }

        return final_url, headers

    def prepare_request(self, gl_merchant_request, final_url, headers):
        request = requests.Request(url=final_url, headers=headers).prepare()

        if gl_merchant_request.get_payload() == self.REQUEST_URI:
            request.prepare_method('GET')
        else:
            request_body = gl_merchant_request.get_payload()
            request.prepare_method('POST')
            request.prepare_body(data=request_body, files=None)

        return request

    @staticmethod
    def create_session(request):
        session = requests.Session()
        session.max_redirects = 0

        return session.send(request)
