# PyGlocalAPIClient
[![codecov](https://codecov.io/gh/PayGlocal-Technologies/payglocal-python-sdk/branch/master/graph/badge.svg?token=C7G7HFUIDT)](https://codecov.io/gh/PayGlocal-Technologies/payglocal-python-sdk)

This is the python implementation of PayGlocal's Glocal API Client. 

**Packages Required:** 
```
jwcrypto
python-jose
coverage
```

### PayGlocal Config File

Once you have the payglocal public key and the required private key downloaded from the Payglocal Portal, you can use them in creating JWE and JWS tokens.
If you want to use a portfolio key instead of a transacting key, please add the portfolio mid in the following line of the payglocal config file.

```ini
glocalMerchant.parentMid = <parent_mid>
```

### Usage

Once you have our public and private key files, move them to the required folder under resources, such that develop, uat and production keys are moved to 
`resources/dev/`, `resources/uat/` and `resources/prod/` folders respectively.

Once they are moved, set the payglocal config file with the following information:
```ini
[Properties]
glocal.merchant.encryptPayload = true
glocal.merchant.sendTransaction = true
glocalMerchant.parentMid = <portfolio mid if any, (optional)>
glocalMerchant.mid = <transacting mid you are using>

glocalMerchant.privateKey.pemFilelLocation = path/to/privatekey.pem
glocalMerchant.privateKey.kid = <kid of merchant private key>
glocal.publicKey.pemFileLocation = path/to/<payglocal public key file>
glocal.publicKey.kid = <kid of glocal public key>

glocalMerchant.status.payload = /gl/v1/payments/<gid>/status -> the gid of the transaction whose status you want to see

logging.level = INFO
```

Once your payload is set in `resources/requestpayload.json` and set the appropriate properties in `resources/payglocalconfig.ini`
The client runs by simply invoking the main.py file. Run the following code in the project directory.

```bash
pip3 install -r requirements.txt
python3 main.py
```

Once you have your JWS Token generated by the python SDK, you can copy and paste the token in the following postman collection: 
https://github.com/PayGlocal-Technologies/payglocal-postman/blob/main/jwt-authN-payment-apis.json

Import the above collection, and replace the jwe token in the body section of the postman calls for any POST methods.
Enter the JWS token for the `x-gl-token-external` in the headers of your requests. 

To test the status call, run the main.py file again with the orderId/gid of the transaction in the payglocal config file
as follows:
`glocalMerchant.status.payload = /gl/v1/payments/<gid>/status`

Use the status call JWS token shown in the output in the header of the get call.

To verify a signature, from payglocal's `x-gl-token` received from merchant callback url etc, you may enter the token in `glocalMerchant.jws.verify.token = <token>`, and run `main.py`
The logs will print out the payload successfully upon verification.

### Running Tests

Tests can be run by running the following code in the project directory.
```bash
python3 -m unittest discover -v
```

### Running Coverage Tests

Coverage Tests can be run by running the following code in the project directory. An HTML page will be initialized in the ```coverage_html``` folder, all coverage information can be accessed through ```index.html```.
```bash
coverage run -m unittest 
coverage html -d coverage_html
```

### Logging

The client can be run at various logging levels, and can be configured by setting the following parameter in the payglocal config file.
```ini
logging.level =
```
The parameter can take the following values for logging level.
```properties
CRITICAL
ERROR
WARNING
INFO (default)
DEBUG
```
