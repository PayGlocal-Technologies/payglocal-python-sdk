from unittest import TestCase
from properties_reader import PropertiesFile


class TestPropertiesFile(TestCase):
    def test_get_property(self):
        self.assertEqual(PropertiesFile().get_property('glocal.merchant.encryptPayload'), 'true')
