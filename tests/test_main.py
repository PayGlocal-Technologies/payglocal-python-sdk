from unittest import TestCase, mock

import api_auth_helper
import http_client
from main import GlocalApiClient


class TestGlocalApiClient(TestCase):
    initiate_client = GlocalApiClient(False, None, None)
    refund_client = GlocalApiClient(False, None, '/gl/v1/payments/gl_52822acf-3e0a-44af-be6f-255840bc4a0f/refund')

    initiate_return_value_json = {
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

    refund_return_value_json = {
        "gid": "gl_1e27d51c-342d-40e7-b643-fe84604fbb1a",
        "status": "SENT_FOR_REFUND",
        "message": "Refund request sent successfully",
        "timestamp": "02/12/2021 19:46:34",
        "reasonCode": "GL-201-001",
        "data":
            {
                "merchantTxnId": "23AEE8CB6B62EE2AF07",
                "refundCurrency": "INR",
                "refundAmount": "10.00"
            },
        "errors": None
    }

    response_mock_headers = {
        'Content-Type': 'application/json'
    }

    def test_get_http_client_helper(self):
        self.assertIsInstance(self.initiate_client.get_http_client_helper(), type(http_client.HttpClient('', '')))

    def test_get_api_auth_helper(self):
        self.assertIsInstance(self.initiate_client.get_api_auth_helper(), type(api_auth_helper.ApiAuthHelper()))

    @mock.patch('time.time', mock.MagicMock(return_value=12345))
    def test_initiate_payment(self):
        with mock.patch('requests.Session.send') as mocker:
            resp_mock = mock.Mock
            resp_mock.json = mock.Mock(return_value=self.initiate_return_value_json)
            resp_mock.headers = self.response_mock_headers

            response_from_mock_initiate_call = self.initiate_client.initiate_payment()

            self.assertEqual(response_from_mock_initiate_call.json()['status'], 'INPROGRESS')
            assert mocker.called

        with mock.patch('requests.Session.send') as mocker:
            resp_mock = mock.Mock
            resp_mock.json = mock.Mock(return_value=self.refund_return_value_json)
            resp_mock.headers = self.response_mock_headers

            response_from_mock_refund_call = self.initiate_client.initiate_payment()

            self.assertEqual(response_from_mock_refund_call.json()['status'], 'SENT_FOR_REFUND')
            assert mocker.called
