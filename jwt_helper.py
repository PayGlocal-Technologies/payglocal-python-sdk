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
    parent_mid = GLOCAL_PROPERTIES.get_property('glocalMerchant.parentMid')
    is_payload_encrypted = GLOCAL_PROPERTIES.get_property('glocal.merchant.encryptPayload')

    log_level = GLOCAL_PROPERTIES.get_property('logging.level')
    log_level = log_level if log_level is not None else log.INFO
    log.basicConfig(level=log_level)

    def create_jws_token_with_rsa(self, payload, private_key):
        """
        Function to create JWS token
        :param payload: JWE Token
        :param private_key: Private key of the merchant (Downloaded form gcc portal), it will be the transacting mid's
        key if there is no portfolio/parent key, otherwise, if parent/portfolio mid is present, then the parent/portfolio
        key used must be used

        Create JWE headers with some custom parameters
         -> x-gl-merchantId : merchantId of whose key is given
         -> x-gl-enc : is Payload encrypted (should be set as true)
         -> issued-by : required merchant id will be used
         -> is-digested : is payload digested (should be set as true)

        Creating claimSet for JWS token
         -> digest : digest of the payload
         -> digestAlgorithm : SHA-256
         -> iat : issued at time (it should be token creation time in epoch milliseconds)
         -> exp -> duration of expiry time of the JWE token (it is recommended to use 5 minutes as expiry time)

        :return: JWS Token
        """

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

        if self.parent_mid is not None and self.parent_mid != '':
            jws_headers['issued-by'] = self.parent_mid
            jws_headers['x-gl-kid-mid'] = self.parent_mid

        log.info('Creating JWS token for ' + str(self.merchant_mid))
        digest = hashlib.sha256(payload.encode()).digest()
        digest_decoded = base64.b64encode(digest).decode("utf-8")

        jws_claimset = {
            'digest': digest_decoded,
            'digestAlgorithm': self.DIGEST_ALGORITHM,
            'iat': str(int(time.time() * 1000)),
            'exp': self.TOKEN_EXPIRY_TIME_IN_MILLISECONDS,
        }
        log.info('Created Auth token claim set')

        jws_token = jws.JWS(payload=json.dumps(jws_claimset))
        jws_token.add_signature(key=private_key, protected=jws_headers)
        log.info("Signed the Auth token.")
        return jws_token.serialize(compact=True)

    def create_jwe_token(self, payload, public_key):
        """
        Function to create JWE token
        :param payload : non-encrypted payload (json stringified)
        :param public_key : Public key of PayGlocal (Downloaded form gcc portal)

        Create JWE headers with some custom parameters
         -> iat : issued at time (it should be token creation time in epoch milliseconds)
         -> exp : duration of expiry time of the JWE token (it is recommended to use 5 minutes as expiry time)
         -> issued-by : required merchant id will be used

        :return: JWE Token
        """
        if public_key is None:
            log.error("PayGlocal RSA public key is null.")
            return None

        required_merchant_id = self.parent_mid if self.parent_mid != '' and self.parent_mid is not None \
            else self.merchant_mid

        log.info('Creating JWE token with Glocal Public Key')
        jwe_headers = {
            'alg': self.JWE_ALGORITHM,
            'enc': self.JWE_ENCRYPTION_METHOD,
            'kid': self.glocal_public_key_kid,
            'iat': str(int(time.time()*1000)),
            'exp': self.TOKEN_EXPIRY_TIME_IN_MILLISECONDS,
            'issued-by': required_merchant_id,
            'is-digested': 'true'
        }
        log.info('Created JWE token header for ' + str(required_merchant_id))

        jwe_token = jwe.JWE(payload.encode('utf-8'), json_encode(jwe_headers))
        jwe_token.add_recipient(public_key)
        encrypted_token = jwe_token.serialize(compact=True)
        return encrypted_token
