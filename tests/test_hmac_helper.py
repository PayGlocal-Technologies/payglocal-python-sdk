import base64
import hashlib
import hmac
from unittest import TestCase

from hmac_helper import HmacHelper


class TestHmacHelper(TestCase):

    api_secret = 'test_api_secret'
    request_uri = '/gcc/v2/partner/merchant/onboard/business-category'
    payload = '{"externalOnboardingId":"partner-001","panNumber":"ABCDE1234F"}'

    def expected_digest(self, signing_input):
        return base64.b64encode(
            hmac.new(self.api_secret.encode(), signing_input.encode(), hashlib.sha256).digest()
        ).decode()

    def test_create_digest_for_get_signs_request_uri(self):
        self.assertEqual(HmacHelper().create_digest('GET', self.request_uri, None, self.api_secret),
                         self.expected_digest(self.request_uri))

    def test_create_digest_for_get_with_query_string(self):
        request_uri = self.request_uri + '?page=1'
        self.assertEqual(HmacHelper().create_digest('get', request_uri, None, self.api_secret),
                         self.expected_digest(request_uri))

    def test_create_digest_for_post_signs_payload(self):
        self.assertEqual(HmacHelper().create_digest('POST', '/gcc/v2/partner/merchant/onboard', self.payload,
                                                    self.api_secret),
                         self.expected_digest(self.payload))

    def test_create_digest_for_put_signs_payload(self):
        self.assertEqual(HmacHelper().create_digest('PUT', '/gcc/v2/partner/merchant/onboard', self.payload,
                                                    self.api_secret),
                         self.expected_digest(self.payload))

    def test_create_digest_without_secret(self):
        self.assertIsNone(HmacHelper().create_digest('GET', self.request_uri, None, None))
        self.assertIsNone(HmacHelper().create_digest('GET', self.request_uri, None, ''))

    def test_create_digest_without_signing_input(self):
        self.assertIsNone(HmacHelper().create_digest('POST', self.request_uri, None, self.api_secret))
        self.assertIsNone(HmacHelper().create_digest('GET', None, self.payload, self.api_secret))
