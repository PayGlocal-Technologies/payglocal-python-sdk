import base64
import hashlib
import hmac
from unittest import TestCase

from hmac_helper import HmacHelper


class TestHmacHelper(TestCase):

    key = b'0123456789abcdef0123456789abcdef'
    salt = base64.b64encode(key).decode()
    request_uri = '/gcc/v2/partner/merchant/onboard/business-category'
    payload = '{"externalOnboardingId":"partner-001","panNumber":"ABCDE1234F"}'

    def expected_digest(self, signing_input):
        return base64.b64encode(
            hmac.new(self.key, signing_input.encode(), hashlib.sha256).digest()
        ).decode()

    def test_create_digest_for_get_signs_request_uri(self):
        self.assertEqual(HmacHelper().create_digest('GET', self.request_uri, None, self.salt),
                         self.expected_digest(self.request_uri))

    def test_create_digest_for_get_with_query_string(self):
        request_uri = self.request_uri + '?page=1'
        self.assertEqual(HmacHelper().create_digest('get', request_uri, None, self.salt),
                         self.expected_digest(request_uri))

    def test_create_digest_for_post_signs_payload(self):
        self.assertEqual(HmacHelper().create_digest('POST', '/gcc/v2/partner/merchant/onboard', self.payload,
                                                    self.salt),
                         self.expected_digest(self.payload))

    def test_create_digest_for_put_signs_payload(self):
        self.assertEqual(HmacHelper().create_digest('PUT', '/gcc/v2/partner/merchant/onboard', self.payload,
                                                    self.salt),
                         self.expected_digest(self.payload))

    def test_create_digest_uses_decoded_salt_not_salt_string(self):
        string_key_digest = base64.b64encode(
            hmac.new(self.salt.encode(), self.request_uri.encode(), hashlib.sha256).digest()
        ).decode()
        self.assertNotEqual(HmacHelper().create_digest('GET', self.request_uri, None, self.salt), string_key_digest)

    def test_create_digest_without_salt(self):
        self.assertIsNone(HmacHelper().create_digest('GET', self.request_uri, None, None))
        self.assertIsNone(HmacHelper().create_digest('GET', self.request_uri, None, ''))

    def test_create_digest_with_invalid_salt(self):
        self.assertIsNone(HmacHelper().create_digest('GET', self.request_uri, None, 'not base64!'))

    def test_create_digest_without_signing_input(self):
        self.assertIsNone(HmacHelper().create_digest('POST', self.request_uri, None, self.salt))
        self.assertIsNone(HmacHelper().create_digest('GET', None, self.payload, self.salt))
