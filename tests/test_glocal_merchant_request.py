from unittest import TestCase
from glocal_merchant_request import GlocalMerchantRequest


class TestGlocalMerchantRequest(TestCase):
    internal_token = 'internal-token'
    payload = 'payload'

    def test_get_payload(self):
        glocal_merchant_request = GlocalMerchantRequest(self.internal_token, self.payload)
        self.assertEqual(glocal_merchant_request.get_payload(), self.payload)

    def test_get_xgl_token_external(self):
        glocal_merchant_request = GlocalMerchantRequest(self.internal_token, self.payload)
        self.assertEqual(glocal_merchant_request.get_xgl_token_external(), self.internal_token)

    def test_set_xgl_token_external(self):
        glocal_merchant_request = GlocalMerchantRequest(self.internal_token, self.payload)
        new_token = 'new_token'
        glocal_merchant_request.set_xgl_token_external(new_token)
        self.assertEqual(glocal_merchant_request.get_xgl_token_external(), new_token)

    def test_set_payload(self):
        glocal_merchant_request = GlocalMerchantRequest(self.internal_token, self.payload)
        new_payload = 'new_payload'
        glocal_merchant_request.set_payload(new_payload)
        self.assertEqual(glocal_merchant_request.get_payload(), new_payload)
