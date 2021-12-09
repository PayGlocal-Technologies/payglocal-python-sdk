# PyGlocalAPIClient

This is the python implementation of PayGlocal's Glocal API Client. 

**Packages Required:** 
```
requests
jwcrypto
python-jose
coverage
```

### PayGlocal Config File

Uncomment the following lines to perform an initiate call

```ini
glocal.servicename = INITIATE
glocal.apiendpoint.uri = /gl/v1/payments/initiate
```

Uncomment the following lines to perform a refund call

```ini
glocal.servicename = REFUND
glocal.apiendpoint.uri = /gl/v1/payments/{gid-of-the-transaction-to-be-refunded}/refund
```

Uncomment one of the following lines to choose the payglocal environment to test on:

```ini
;glocal.apiendpoint.baseurl = http://localhost:8081
;glocal.apiendpoint.baseurl = https://api.dev.payglocal.in
;glocal.apiendpoint.baseurl = https://api.uat.payglocal.in
#glocal.apiendpoint.baseurl = https://api.prod.payglocal.in
```

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


### Usage

The client runs by simply invoking the main.py file. Run the following code in the project directory.
```bash
python3 main.py
```

### Logging

The client can be run at various logging levels, and can be configured by setting the following parameter.
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
NOTSET
```