import base64
import hashlib
import json
import time
from unittest import TestCase, mock

from jwcrypto import jwe, jws
from jwcrypto.common import json_encode
from jose import jwe as jjwe
from jose import jwt as jjwt

import pem_file_helper
from glocal_merchant_request import GlocalMerchantRequest
from api_auth_helper import ApiAuthHelper


class TestApiAuthHelper(TestCase):

    api_auth = ApiAuthHelper()
    request_uri = '/gl/v1/payments/initiate'
    payload = {
        "merchantTxnId": "23AEE8CB6B62EE2AF07",
        "paymentData": {
            "totalAmount": "10.00",
            "txnCurrency": "INR",
            "cardData": {
                "number": "4111111145551142",
                "expiryMonth": "08",
                "expiryYear": "2023",
                "type": "visa",
                "securityCode": "123"
            },
            "billingData": {
                "firstName": "nihal",
                "lastName": "nihsl8",
                "addressStreet1": "Street 1",
                "addressStreet2": "Near Complex 2",
                "addressCity": "Bangalore",
                "addressState": "Karnataka",
                "addressPostalCode": "7667",
                "addressCountry": "IN",
                "emailId": "something@gmail.com"
            }
        },
        "merchantCallbackURL": "https://api.dev.payglocal.in/gl/v1/payments/merchantCallback",
        "refundType": "F"
    }
    pem = pem_file_helper.PemFileHelper()
    private_key = pem.get_private_key()
    public_key = pem.get_pubic_key()

    def create_expected_payload(self):
        jwe_headers = {
            'alg': jjwe.ALGORITHMS.RSA_OAEP_256,
            'enc': jjwe.ALGORITHMS.A128CBC_HS256,
            'kid': '1c2a4b36-5449-4ed3-90a6-0a7999874234',
            'iat': str(int(time.time() * 1000)),
            'exp': 300000,
            'issued-by': 'sakshidomestic',
            'is-digested': 'true'
        }

        jwe_token = jwe.JWE(json.dumps(self.payload).encode('utf-8'), json_encode(jwe_headers))
        jwe_token.add_recipient(self.public_key)
        return jwe_token.serialize(compact=True)

    def create_expected_auth_bearer_token(self, payload):
        jws_headers = {
            'alg': jjwt.ALGORITHMS.RS256,
            'kid': 'c0f6da59-c64f-478b-9f13-a22314b232e6',
            'x-gl-merchantId': 'sakshidomestic',
            'x-gl-enc': 'true',
            'issued-by': 'sakshidomestic',
            'is-digested': 'true'
        }

        digest = hashlib.sha256(json.dumps(payload).encode()).digest()
        digest_decoded = base64.b64encode(digest).decode("utf-8")

        jws_claimset = {
            'digest': digest_decoded,
            'digestAlgorithm': "SHA-256",
            'iat': str(int(time.time() * 1000)),
            'exp': 300000,
        }

        jws_token = jws.JWS(payload=json.dumps(jws_claimset))
        jws_token.add_signature(key=self.private_key, protected=jws_headers)
        return jws_token.serialize(True)

    def test_create_glocal_merchant_request(self):
        self.assertEqual(self.api_auth.create_glocal_merchant_request(None), self.request_uri)
        self.assertEqual(self.api_auth.create_glocal_merchant_request(self.payload), self.payload)

    @mock.patch('time.time', mock.MagicMock(return_value=12345))
    def test_create_payload(self):
        encrypted_payload = self.create_expected_payload()
        self.assertEqual(self.api_auth.create_payload(json.dumps(self.payload)).get_payload().split('.')[0],
                         encrypted_payload.split('.')[0])

        self.api_auth.pem_file_helper.merchant_public_key = None
        self.assertIsNone(self.api_auth.create_payload(json.dumps(self.payload)))
        self.api_auth.encrypt_payload = False
        self.assertEqual(self.api_auth.create_payload(json.dumps(self.payload)).get_payload(),
                         json.dumps(self.payload))

    @mock.patch('time.time', mock.MagicMock(return_value=12345))
    def test_create_and_set_auth_bearer_token(self):
        encrypted_payload = self.create_expected_payload()
        auth_token = self.create_expected_auth_bearer_token(encrypted_payload)

        gl_merchant_req_actual = GlocalMerchantRequest(None, encrypted_payload)
        gl_merchant_req_actual = self.api_auth.create_and_set_auth_bearer_token(gl_merchant_req_actual)
        self.assertEqual(gl_merchant_req_actual.xgl_token_external.split('.')[0], auth_token.split('.')[0])

        self.api_auth.pem_file_helper.merchant_private_key = None
        gl_merchant_req_actual = self.api_auth.create_and_set_auth_bearer_token(gl_merchant_req_actual)
        self.assertIsNone(gl_merchant_req_actual)
