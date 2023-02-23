from unittest import TestCase

from jwcrypto import jwk

import pem_file_helper


class TestPemFileHelper(TestCase):

    pem = pem_file_helper.PemFileHelper()

    def test_set_private_key_from_pem_file(self):
        self.pem.private_key_pem_file_location = "resources/keys/test/privatekey.pem"
        private_key = self.pem.set_private_key_from_pem_file()
        expected_private_key_details = {
            "kid": "FxlWkoXzPk5m9-FuxjW7vRAGxNkT7MoxZGyhV2xjgYw",
            "thumbprint": "FxlWkoXzPk5m9-FuxjW7vRAGxNkT7MoxZGyhV2xjgYw",
            "kty": "RSA",
            "n": "43WyOeBlUTACUIdEw0HlL5N12FibPKlj9Ia_f07Rzm5V94_3QMynf2iwwzHTadHM5yku-wFcTM0LyTu6wEp6WIa9dKPdIQhMvs"
                 + "NAgf9rN9KKeyb0usvZt54qOzuDPaaauY2pD2als2WNXBZd3CgrWqZmom-MPknFcfkhT4zl7LOnBbMzIn0v4sd5jjBF-xExxwkmK"
                 + "riuCN_4luK7Wm5iWNTSqOiciMCOey-l3rhxDUZT8BmCE6PM8wDUercHNyoj3najQwxG09wVS2m2joQArk-y9mYfJKffIS70iyFw"
                 + "aD1O7lzNPyn2Cm8FP_Z0mCg_JOHgM4ZaR63mPGk9cfRdoQ",
            "e": "AQAB"
        }
        expected_private_key = jwk.JWK(**expected_private_key_details)
        self.assertEqual(private_key, expected_private_key)

    def test_set_public_key_from_pem_file(self):
        public_key = self.pem.set_public_key_from_pem_file()
        expected_public_key_details = {
            "kid": "stU_K9M99AU8WVS1-pHpcw02XanpwOWSwhQBQk8MaaM",
            "thumbprint": "stU_K9M99AU8WVS1-pHpcw02XanpwOWSwhQBQk8MaaM",
            "kty": "RSA",
            "n": "23_ittMCVfOApzuZWeWQk0iPFMe41lmAURF8lFTQIK6JXWHDmQUfg0_iES9NpS7oVwVucS5i0rJz09cBMQ9g9XSVYwaYPWm-2Lc2-"
                 + "pXimYCxrTFx1_eY51HlgKV9M-b-dJboyOWuGeyFUM3OVxQEB6UN5XOKHtcRFFkIYtXbBDBsbDte7dWMQYHG75TYa-37WVHbzvoJ"
                 + "Op5luK_AJrY4Z0SZgV5mGWGVz17UoilRJipXXvV7IeDXZDgTqQG1dYAXISN3ajAdkQVGgrVBf9Q4zVWrFaDq8RfrbVGbWVwFNl"
                 + "JLIP-Kotl5XprHLD7hh9M8MG3FY4BWI-XDc7TegHk7dw",
            "e": "AQAB"
        }
        expected_public_key = jwk.JWK(**expected_public_key_details)
        self.assertEqual(public_key, expected_public_key)

    def test_get_pubic_key(self):
        public_key = self.pem.get_public_key()
        expected_public_key_details = {
            "kid": "stU_K9M99AU8WVS1-pHpcw02XanpwOWSwhQBQk8MaaM",
            "thumbprint": "stU_K9M99AU8WVS1-pHpcw02XanpwOWSwhQBQk8MaaM",
            "kty": "RSA",
            "n": "23_ittMCVfOApzuZWeWQk0iPFMe41lmAURF8lFTQIK6JXWHDmQUfg0_iES9NpS7oVwVucS5i0rJz09cBMQ9g9XSVYwaYPWm-2Lc2-"
                 + "pXimYCxrTFx1_eY51HlgKV9M-b-dJboyOWuGeyFUM3OVxQEB6UN5XOKHtcRFFkIYtXbBDBsbDte7dWMQYHG75TYa-37WVHbzvoJ"
                 + "Op5luK_AJrY4Z0SZgV5mGWGVz17UoilRJipXXvV7IeDXZDgTqQG1dYAXISN3ajAdkQVGgrVBf9Q4zVWrFaDq8RfrbVGbWVwFNl"
                 + "JLIP-Kotl5XprHLD7hh9M8MG3FY4BWI-XDc7TegHk7dw",
            "e": "AQAB"
        }
        expected_public_key = jwk.JWK(**expected_public_key_details)
        self.assertEqual(public_key, expected_public_key)

    def test_get_private_key(self):
        self.pem.private_key_pem_file_location = "resources/keys/test/privatekey.pem"
        private_key = self.pem.set_private_key_from_pem_file()
        expected_private_key_details = {
            'd': 'erXYPNkOT8pytTcEpcI6_nuzK9BBj2xi_FxlmyzOi2uC_VexsEe4ZUf5dJTA1WnV_S9-pPOK8_P608lharPDZVbrhq2Qcm2j2ZZE'
                 'it1c3nS7OM0_YjbvcdvmNKZamzvyZQBDoIdkBXBX3sJCSK9zFCiJXkCHjGMIHgClM-FzeUo-BDlBZhILgy1mfIlFwMnzYyL1UHa88'
                 'gt61XFPD9eWEvPhnvkiYYS7904utxujYK54svF-59_yXWVyQfI7KalYedx1AlH0jF9sQ7J4WrBYYaOJhiq5gV16w5RtOoJghZ2aI'
                 'hTL9Thg0XhnlWuR_L4y79G5jwZcjKCSxCuX2O9OMQ',
            'dp': 'WshkCA36RgpLyJ5pLrYxLC0VuvyU8_sCvHU6WBdlcV1OiTDPmLX96CKuTqFZr6qzXK8RjRxjcJJi5tMhm8N-p5TCFltraf2-dzP'
                  '0UqIoJjzvaSGOUPfyBdtw5sEcUjYniXQdKHCcicEd3qcgscVORdJPw33bzX72lXwxsNmCyY8',
            'dq': 'u6meNGPhWjcWE-012mQJSCUeTdTqcShZexNs70IKCFVJoIv7hbYP9txU-7I5cudjb45UWA_7vzaT2a2v1yKwTTFGZVY23eG2cz2'
                  'x32--C-sajFA3B1xBWxXD2-tSzAOGljyd8wnk6b06RCC5AZ_iXZeDET6W9AyMlN0yWIykfCM',
            'e': 'AQAB',
            'kid': 'FxlWkoXzPk5m9-FuxjW7vRAGxNkT7MoxZGyhV2xjgYw',
            'kty': 'RSA',
            'n': '43WyOeBlUTACUIdEw0HlL5N12FibPKlj9Ia_f07Rzm5V94_3QMynf2iwwzHTadHM5yku-wFcTM0LyTu6wEp6WIa9dKPdIQhMvsNA'
                 'gf9rN9KKeyb0usvZt54qOzuDPaaauY2pD2als2WNXBZd3CgrWqZmom-MPknFcfkhT4zl7LOnBbMzIn0v4sd5jjBF-xExxwkmKriu'
                 'CN_4luK7Wm5iWNTSqOiciMCOey-l3rhxDUZT8BmCE6PM8wDUercHNyoj3najQwxG09wVS2m2joQArk-y9mYfJKffIS70iyFwaD1O'
                 '7lzNPyn2Cm8FP_Z0mCg_JOHgM4ZaR63mPGk9cfRdoQ',
            'p': '85uSHLh23X0vCr76gj3nr5B-CQ9FgvNFoDc_hhevK9_snRihWoyMT_ZXHldxilWAWD3IbT3xhigDs8v45xM3vmCDmgwy1MYybY-'
                 '7z469lIechvmxz3NScDFgt__yySHSkTaAfkNIgd4OO2ap4SQnEUUU_kQ63BYjfxn53lg7p0M',
            'q': '7wfV6wERhNc85i3VGZkTstVT_qSO53rpLMc8TOowcUbf5JBJkKDVaPpNaFr55pmF6HSGEcikgMuRxBf9Mq1e2IIOJzMIqaUFbtP8'
                 '8NaHAE8pQhooTwaiwy5e3qA2P6Woz0WVBFUy4bmtcdjtwcMSLrp95EZ5BnDQ0LKX8qkt30s',
            'qi': 'ipmXLLoJMJDYbo256jQB0p6q9hU3f8RusPoAJ354s6-3g8u19cMzAWvNMUgG2U2BEMKm6O5I3fsh5Sd4wR3xDhEzjUVkPCrHKh'
                  'rT_scHd0gljNFsp7elZ6JkhbVZXwLA-Fp08frLMFrgP2-oOQ-DS4MWZe1OauMy4e_fHt2C1mg'
        }
        expected_private_key = jwk.JWK(**expected_private_key_details)
        self.assertEqual(private_key, expected_private_key)
