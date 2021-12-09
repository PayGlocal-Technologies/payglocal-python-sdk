from unittest import TestCase, mock

from http_client import HttpClient
from glocal_merchant_request import GlocalMerchantRequest


class TestHttpClient(TestCase):
    base_url = 'https://api.dev.payglocal.in'
    request_uri = '/gl/v1/payments/initiate'

    final_url_exp = base_url + request_uri
    headers_exp = {
        'x-gl-token-external': "x-gl-token-external",
        'Content-Type': 'text/plain'
    }

    return_value_json = {
        'gid': 'gl_a0f33682-dbac-420a-b83d-00ea3fd16873',
        'status': 'INPROGRESS',
        'message': 'Transaction Created Successfully',
        'timestamp': '08/12/2021 18:00:50',
        'reasonCode': 'GL-201-001',
        'data': {
            'redirectUrl': 'https://api.dev.payglocal.in/gl/v1/payments/redirect?x-gl-token=eyJpc3N1ZWQtYnkiOiJHbG9jYW'
                           'wiLCJpcy1kaWdlc3RlZCI6ImZhbHNlIiwiYWxnIjoiUlMyNTYiLCJraWQiOiIxYzJhNGIzNi01NDQ5LTRlZDMtOTB'
                           'hNi0wYTc5OTk4NzQyMzQifQ.eyJpYXQiOiIxNjM4OTY2NjQ4ODE3IiwieC1nbC1lbmMiOiJ0cnVlIiwieC1nbC1naW'
                           'QiOiJnbF9hMGYzMzY4Mi1kYmFjLTQyMGEtYjgzZC0wMGVhM2ZkMTY4NzMiLCJ4LWdsLW1lcmNoYW50SWQiOiJzYWt'
                           'zaGlkb21lc3RpYyJ9.B3SsjJ2eJeZCW0PfkyHrovE3xGw7eo5xHRkOrKTHZpYkf-im0YNOozV8_DDQdYcf3cQs-kp'
                           'YFjxR6M8o-a1UxTRZ7F0TSIMUWPPGrWPjjZ-QrgN5aV7QC84EK-62C0fXwzZ6bYMvqmsAj7TD3TWLYr4atSdfPY8qK'
                           'hnBFeM6wV4nXyNsD6UNY3k3AgNy9KWUelHoFgQijea4i29401EhJhd20UHh3ryBQX0yfricZQ72P8cPuMVUMUTXJha'
                           'hbMMJtz6HxTL-uON431iaLdD9_1O-G6I7RX3WQEJc5fXwVse8iDAhKZNZQ7T1LjraT3KcDucz0oQtxI3FohwScegTAw'
            ,
            'statusUrl': 'https://api.dev.payglocal.in/gl/v1/payments/gl_a0f33682-dbac-420a-b83d-00ea3fd16873/status?'
                         'x-gl-token=eyJpc3N1ZWQtYnkiOiJHbG9jYWwiLCJpcy1kaWdlc3RlZCI6ImZhbHNlIiwiYWxnIjoiUlMyNTYiLCJr'
                         'aWQiOiIxYzJhNGIzNi01NDQ5LTRlZDMtOTBhNi0wYTc5OTk4NzQyMzQifQ.eyJpYXQiOiIxNjM4OTY2NjQ4ODE3Iiwi'
                         'eC1nbC1lbmMiOiJ0cnVlIiwieC1nbC1naWQiOiJnbF9hMGYzMzY4Mi1kYmFjLTQyMGEtYjgzZC0wMGVhM2ZkMTY4NzMi'
                         'LCJ4LWdsLW1lcmNoYW50SWQiOiJzYWtzaGlkb21lc3RpYyJ9.B3SsjJ2eJeZCW0PfkyHrovE3xGw7eo5xHRkOrKTHZpY'
                         'kf-im0YNOozV8_DDQdYcf3cQs-kpYFjxR6M8o-a1UxTRZ7F0TSIMUWPPGrWPjjZ-QrgN5aV7QC84EK-62C0fXwzZ6bYMv'
                         'qmsAj7TD3TWLYr4atSdfPY8qKhnBFeM6wV4nXyNsD6UNY3k3AgNy9KWUelHoFgQijea4i29401EhJhd20UHh3ryBQX0y'
                         'fricZQ72P8cPuMVUMUTXJhahbMMJtz6HxTL-uON431iaLdD9_1O-G6I7RX3WQEJc5fXwVse8iDAhKZNZQ7T1LjraT3K'
                         'cDucz0oQtxI3FohwScegTAw'
            },
        'errors': None
        }

    response_mock_headers = {
        'Content-Type': 'application/json'
    }

    def test_initiate_request(self):
        http_client = HttpClient(self.base_url, self.request_uri)
        x_gl_token_external = "x-gl-token-external"
        payload = "payload"
        gl_merchant_request = GlocalMerchantRequest(x_gl_token_external, payload)
        final_url, headers = http_client.initiate_request(gl_merchant_request)

        self.assertEqual(final_url, self.final_url_exp)
        self.assertEqual(headers, self.headers_exp)

    def test_prepare_request(self):
        http_client = HttpClient(self.base_url, self.request_uri)
        self.assertEqual(http_client.prepare_request(GlocalMerchantRequest("x-gl-token-external", "payload"),
                                                     self.final_url_exp, self.headers_exp).method, "POST")
        self.assertEqual(http_client.prepare_request(GlocalMerchantRequest("x-gl-token-external", "payload"),
                                                     self.final_url_exp, self.headers_exp).body, "payload")
        self.assertEqual(http_client.prepare_request(GlocalMerchantRequest("x-gl-token-external", self.request_uri),
                                                     self.final_url_exp, self.headers_exp).method, "GET")

    def test_create_session(self):
        http_client = HttpClient(self.base_url, self.request_uri)
        request = http_client.prepare_request(GlocalMerchantRequest("x-gl-token-external", "payload"),
                                              self.final_url_exp, self.headers_exp)

        with mock.patch('requests.Session.send') as mocker:
            resp_mock = mock.Mock
            resp_mock.json = mock.Mock(return_value=self.return_value_json)
            resp_mock.headers = self.response_mock_headers

            resp = http_client.create_session(request)

            self.assertEqual(resp.json()['status'], 'INPROGRESS')
            assert mocker.called
