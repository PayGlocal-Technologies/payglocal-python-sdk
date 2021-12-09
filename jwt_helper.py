import base64
import hashlib
import json
import logging as log
import time

from jwcrypto import jwe, jws
import jose.jwt
import jose.jwe
import jose.jwk
from jwcrypto.common import json_encode

from properties_reader import PropertiesFile


class JwtHelper:

    DIGEST_ALGORITHM = "SHA-256"
    JWS_ALGORITHM = jose.jwt.ALGORITHMS.RS256
    JWE_ALGORITHM = jose.jwe.ALGORITHMS.RSA_OAEP_256
    JWE_ENCRYPTION_METHOD = jose.jwe.ALGORITHMS.A128CBC_HS256
    TOKEN_EXPIRY_TIME_IN_MILLISECONDS = 300000
    GLOCAL_PROPERTIES = PropertiesFile()

    merchant_private_key_kid = GLOCAL_PROPERTIES.get_property('glocalMerchant.privateKey.kid')
    glocal_public_key_kid = GLOCAL_PROPERTIES.get_property('glocal.publicKey.kid')
    merchant_mid = GLOCAL_PROPERTIES.get_property('glocalMerchant.mid')
    is_payload_encrypted = GLOCAL_PROPERTIES.get_property('glocal.merchant.encryptPayload')

    log_level = GLOCAL_PROPERTIES.get_property('logging.level')
    log_level = log_level if log_level is not None else log.INFO
    log.basicConfig(level=log_level)

    def create_jws_token_with_rsa(self, payload, private_key):
        if private_key is None:
            log.error("Merchant RSA private key is null.")
            return None

        jws_headers = {
            'alg': self.JWS_ALGORITHM,
            'kid': self.merchant_private_key_kid,
            'x-gl-merchantId': self.merchant_mid,
            'x-gl-enc': self.is_payload_encrypted,
            'issued-by': self.merchant_mid,
            'is-digested': 'true'
        }

        return self.create_jws_token(payload, private_key, jws_headers)

    def create_jws_token(self, payload, private_key, headers):
        log.info('Creating JWS token')

        digest = hashlib.sha256(payload.encode()).digest()
        digest_decoded = base64.b64encode(digest).decode("utf-8")

        jws_claimset = {
            'digest': digest_decoded,
            'digestAlgorithm': self.DIGEST_ALGORITHM,
            'iat': str(int(time.time()*1000)),
            'exp': self.TOKEN_EXPIRY_TIME_IN_MILLISECONDS,
        }

        jws_token = jws.JWS(payload=json.dumps(jws_claimset))
        jws_token.add_signature(key=private_key, protected=headers)

        return jws_token.serialize(compact=True)

    def create_jwe_token(self, payload, public_key):
        log.info('Creating JWE token with Glocal Public Key')

        if public_key is None:
            log.error("PayGlocal RSA public key is null.")
            return None

        jwe_headers = {
            'alg': self.JWE_ALGORITHM,
            'enc': self.JWE_ENCRYPTION_METHOD,
            'kid': self.glocal_public_key_kid,
            'iat': str(int(time.time()*1000)),
            'exp': self.TOKEN_EXPIRY_TIME_IN_MILLISECONDS,
            'issued-by': self.merchant_mid,
            'is-digested': 'true'
        }

        jwe_token = jwe.JWE(payload.encode('utf-8'), json_encode(jwe_headers))
        jwe_token.add_recipient(public_key)
        encrypted_token = jwe_token.serialize(compact=True)
        return encrypted_token
