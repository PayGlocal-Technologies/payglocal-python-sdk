from jwcrypto import jwk

from properties_reader import PropertiesFile


class PemFileHelper:

    properties = PropertiesFile()
    private_key_pem_file_location = properties.get_property('glocalMerchant.privateKey.pemFilelLocation')
    public_key_pem_file_location = properties.get_property('glocal.publicKey.pemFileLocation')

    def __init__(self):
        self.merchant_private_key = self.set_private_key_from_pem_file()
        self.merchant_public_key = self.set_public_key_from_pem_file()

    def set_private_key_from_pem_file(self):
        data = self.read_data(self.private_key_pem_file_location)
        private_key = jwk.JWK().from_pem(data)
        return private_key

    def set_public_key_from_pem_file(self):
        data = self.read_data(self.public_key_pem_file_location)
        public_key = jwk.JWK().from_pem(data)
        return public_key

    def get_public_key(self):
        return self.merchant_public_key

    def get_private_key(self):
        return self.merchant_private_key

    @staticmethod
    def read_data(location):
        with open(location, "rb") as f:
            data = f.read()
            f.close()

        return data
