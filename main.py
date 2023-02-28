import json
import logging as log

from jwt_helper import JwtHelper
from pem_file_helper import PemFileHelper
from properties_reader import PropertiesFile

PAYLOAD_JSON_FILE_PATH = 'resources/requestpayload.json'
properties = PropertiesFile()
status_payload = properties.get_property('glocalMerchant.status.payload')
jws_token_to_be_verified = properties.get_property('glocalMerchant.jws.verify.token')

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
        log.info('Successfully create JWE token for payment services (Payment initiation/Refund), as a part of the '
                 'request body of POST endpoint.')
        log.info('JWE token for request body use (POST endpoints) = ' + jwe_token)

        jws_token = jwt_helper.create_jws_token_with_rsa(jwe_token, pem_file_helper.get_private_key())
        log.info('Successfully create JWS token for payment services (Payment initiation/Refund)')
        log.info('JWS token for request parameter use = ' + jws_token)

        # for status service, digested payload is requestUri
        jws_token_status = jwt_helper.create_jws_token_with_rsa(status_payload, pem_file_helper.get_private_key())
        log.info("JWS token for Status call = " + jws_token_status)

        # for jws verification
        if jws_token_to_be_verified is not None and jws_token_to_be_verified != '':
            log.info("JWS Token to be verified is present as {" + jws_token_to_be_verified + "}, verifying token...")
            is_verified = jwt_helper.verify_jwt_token(jws_token_to_be_verified, pem_file_helper.get_public_key())
            if is_verified:
                log.info("JWS token is verified from Payglocal!")
            else:
                log.error("JWS token verification is unsuccessful!")
        else:
            log.info("No JWS Token to be verified.")

    except RuntimeError as e:
        log.error("Error wile creating/verifying jwe/jws token", e)
