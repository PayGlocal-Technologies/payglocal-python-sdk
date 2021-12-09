import configparser

PROPERTIES_FILE_PATH = 'resources/payglocalconfig.ini'


def read_properties_file():
    config = configparser.RawConfigParser()
    config.read(PROPERTIES_FILE_PATH)
    return config


class PropertiesFile:
    config = read_properties_file()

    def get_property(self, name):
        return self.config.get('Properties', name)
