import logging as log

from jwt_helper import JwtHelper
from pem_file_helper import PemFileHelper
from properties_reader import PropertiesFile
from glocal_merchant_request import GlocalMerchantRequest


class ApiAuthHelper:

    properties = PropertiesFile()

    log_level = properties.get_property('logging.level')
    log_level = log_level if log_level is not None else log.INFO
    log.basicConfig(level=log_level)

    def __init__(self):
        self.jwt_helper = JwtHelper()
        self.pem_file_helper = PemFileHelper()
        self.encrypt_payload = self.properties.get_property('glocal.merchant.encryptPayload').casefold() \
            == "true".casefold()
        self.request_uri = self.properties.get_property('glocal.apiendpoint.uri')

    def create_glocal_merchant_request(self, current_txn_request):
        if current_txn_request is None:
            payload_to_be_digested = self.request_uri
        else:
            payload_to_be_digested = current_txn_request

        return payload_to_be_digested

    def create_payload(self, payload_to_be_digested):
        gl_merchant_request = GlocalMerchantRequest(None, None)

        if self.encrypt_payload and (payload_to_be_digested != self.request_uri):
            encrypted_payload = self.create_encrypted_payload(payload_to_be_digested)
            if encrypted_payload is None:
                log.error("Unable to create encrypted payload")
                return None
            gl_merchant_request.set_payload(encrypted_payload)

        else:
            gl_merchant_request.set_payload(payload_to_be_digested)

        return gl_merchant_request

    def create_and_set_auth_bearer_token(self, gl_merchant_request):

        auth_token = self.create_auth_bearer_token(gl_merchant_request.get_payload())

        if auth_token is None:
            log.error("Unable to create auth token")
            return None

        gl_merchant_request.set_xgl_token_external(auth_token)
        return gl_merchant_request

    def create_encrypted_payload(self, payload_to_be_digested):
        return self.jwt_helper.create_jwe_token(payload_to_be_digested, self.pem_file_helper.get_pubic_key())

    def create_auth_bearer_token(self, encrypted_payload):
        return self.jwt_helper.create_jws_token_with_rsa(encrypted_payload, self.pem_file_helper.get_private_key())
