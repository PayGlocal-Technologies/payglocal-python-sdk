import json
import logging as log

from api_auth_helper import ApiAuthHelper
from properties_reader import PropertiesFile
from http_client import HttpClient


class GlocalApiClient:

    PAYLOAD_JSON_FILE_PATH = 'resources/requestpayload.json'
    properties = PropertiesFile()

    log_level = properties.get_property('logging.level')
    log_level = log_level if log_level is not None else log.INFO
    log.basicConfig(level=log_level)

    def __init__(self, test_flag, test_payload, refund_uri):
        self.api_auth_helper = ApiAuthHelper()
        self.SEND_TRANSACTION = self.properties.get_property('glocal.merchant.sendTransaction').casefold() \
                                == 'true'.casefold()

        if refund_uri is None:
            self.http_client_helper = HttpClient(self.properties.get_property('glocal.apiendpoint.baseurl'),
                                                 self.properties.get_property('glocal.apiendpoint.uri'))
            self.SERVICE_NAME = self.properties.get_property('glocal.servicename')
        else:
            self.http_client_helper = HttpClient(self.properties.get_property('glocal.apiendpoint.baseurl'),
                                                 refund_uri)
            self.SERVICE_NAME = "REFUND"

        if ("INITIATE" == self.SERVICE_NAME) or ("REFUND" == self.SERVICE_NAME):
            if test_flag:
                self.current_transaction_request = test_payload
            else:
                file = open(self.PAYLOAD_JSON_FILE_PATH)
                json_payload = json.load(file)
                self.current_transaction_request = json.dumps(json_payload)
                file.close()
        else:
            self.current_transaction_request = None
        log.info('API Client Instantiated')

    def get_http_client_helper(self):
        return self.http_client_helper

    def get_api_auth_helper(self):
        return self.api_auth_helper

    def initiate_payment(self):

        payload_to_be_digested = self.api_auth_helper.create_glocal_merchant_request(self.current_transaction_request)
        gl_merchant_request = self.api_auth_helper.create_payload(payload_to_be_digested)
        gl_merchant_request = self.api_auth_helper.create_and_set_auth_bearer_token(gl_merchant_request)

        if gl_merchant_request is None:
            log.warning("Unable to create merchant payment request")

        log.info("x-gl-token-external: " + str(gl_merchant_request.get_xgl_token_external()))
        log.info("Payload: " + str(gl_merchant_request.get_payload()))

        if self.SEND_TRANSACTION:
            log.info("Initiating Payment Flow")
            final_url, headers = self.http_client_helper.initiate_request(gl_merchant_request)
            request = self.http_client_helper.prepare_request(gl_merchant_request, final_url, headers)
            return self.http_client_helper.create_session(request)
        else:
            log.warning("Not sending transaction as per configuration")
            return None


if __name__ == "__main__":
    try:
        glocal_api_client = GlocalApiClient(False, None, None)
        if glocal_api_client.get_http_client_helper() is None or glocal_api_client.get_api_auth_helper() is None:
            log.error("Failed to Start API Client.")

        response_from_initiate_call = glocal_api_client.initiate_payment()
        log.info("Completed Payment Flow.")

        try:
            if response_from_initiate_call is not None:
                log.info("Payment response from PayGlocal servers: " + str(response_from_initiate_call.json()))
        except IOError:
            log.error("Unable to parse the response")
    except RuntimeError:
        log.error("Error in completing transaction")
