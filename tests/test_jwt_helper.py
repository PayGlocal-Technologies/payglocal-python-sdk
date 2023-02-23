import base64
import hashlib
import json
import time
from unittest import TestCase, mock

from jose import jwe as jjwe
from jose import jwt as jjwt
from jwcrypto import jwe, jws
from jwcrypto.common import json_encode

import pem_file_helper
from jwt_helper import JwtHelper


class TestJwtHelper(TestCase):

    pem = pem_file_helper.PemFileHelper()
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

    private_key = pem.get_private_key()
    public_key = pem.get_public_key()

    @mock.patch('time.time', mock.MagicMock(return_value=12345))
    def test_create_jws_token_with_rsa(self):
        jws_headers = {
            'alg': jjwt.ALGORITHMS.RS256,
            'kid': 'c0f6da59-c64f-478b-9f13-a22314b232e6',
            'x-gl-merchantId': 'mid',
            'x-gl-enc': 'true',
            'issued-by': 'mid',
            'is-digested': 'true'
        }

        digest = hashlib.sha256(json.dumps(self.payload).encode()).digest()
        digest_decoded = base64.b64encode(digest).decode("utf-8")

        jws_claimset = {
            'digest': digest_decoded,
            'digestAlgorithm': "SHA-256",
            'iat': str(int(time.time()*1000)),
            'exp': 300000,
        }

        jws_token = jws.JWS(payload=json.dumps(jws_claimset))
        jws_token.add_signature(key=self.private_key, protected=jws_headers)

        self.assertEqual(JwtHelper().create_jws_token_with_rsa(json.dumps(self.payload), self.private_key),
                         jws_token.serialize(compact=True))

    @mock.patch('time.time', mock.MagicMock(return_value=12345))
    def test_create_jwe_token(self):
        jwe_headers = {
            'alg': jjwe.ALGORITHMS.RSA_OAEP_256,
            'enc': jjwe.ALGORITHMS.A128CBC_HS256,
            'kid': '1c2a4b36-5449-4ed3-90a6-0a7999874234',
            'iat': str(int(time.time()*1000)),
            'exp': 300000,
            'issued-by': 'mid',
            'is-digested': 'true'
        }

        jwe_token = jwe.JWE(json.dumps(self.payload).encode('utf-8'), json_encode(jwe_headers))
        jwe_token.add_recipient(self.public_key)
        encrypted_token = jwe_token.serialize(compact=True)
        self.assertEqual(JwtHelper().create_jwe_token(json.dumps(self.payload), self.public_key).split('.')[0],
                         encrypted_token.split('.')[0])
