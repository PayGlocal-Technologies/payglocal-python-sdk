import json
import logging as log

from jwt_helper import JwtHelper
from pem_file_helper import PemFileHelper
from properties_reader import PropertiesFile

PAYLOAD_JSON_FILE_PATH = 'resources/requestpayload.json'
properties = PropertiesFile()
status_payload = properties.get_property('glocalMerchant.status.payload')
log_level = properties.get_property('logging.level')
log_level = log_level if log_level is not None else log.INFO
log.basicConfig(level=log_level)
jwt_helper = JwtHelper()
pem_file_helper = PemFileHelper()


def get_json_payload():
    try:
        file = open(PAYLOAD_JSON_FILE_PATH)
        payload_file = json.load(file)
        payload = json.dumps(payload_file)
        file.close()
        return payload
    except RuntimeError as runtime_error:
        log.error('Error in getting/reading payload file', runtime_error)


if __name__ == "__main__":
    json_payload = get_json_payload()
    try:
        jwe_token = jwt_helper.create_jwe_token(json_payload, pem_file_helper.get_public_key())
        log.info('Successfully create JWE token')
        log.info('JWE token = ' + jwe_token)

        jws_token = jwt_helper.create_jws_token_with_rsa(json_payload, pem_file_helper.get_private_key())
        log.info('Successfully create JWS token')
        log.info('JWS token = ' + jws_token)

        # for status service payload = requestUri
        jws_token_status = jwt_helper.create_jws_token_with_rsa(status_payload, pem_file_helper.get_private_key())
        log.info("JWS token for Status call = " + jws_token_status)

    except RuntimeError as e:
        log.error("Error wile creating jwe/jws token", e)
