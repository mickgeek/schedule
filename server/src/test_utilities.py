import unittest
from utilities import JWTEncoder, JWTDecoder, UserPassword

class JWTTestCase(unittest.TestCase):

    def setUp(self):
        self.encoded_header = b'WzEyMywgMzksIDExNiwgMTIxLCAxMTIsIDM5LCA1OCwgMzIsIDM5LCA3NCwgODcsIDg0LCAzOSwgNDQsIDMyLCAzOSwgOTcsIDEwOCwgMTAzLCAzOSwgNTgsIDMyLCAzOSwgNzIsIDgzLCA1MCwgNTMsIDU0LCAzOSwgMTI1XQ=='
        self.encoded_payload = b'WzEyMywgMzksIDEwMSwgMTIwLCAxMTIsIDM5LCA1OCwgMzIsIDUzLCA0OCwgNDgsIDQ4LCA0OCwgNDgsIDQ4LCA0OCwgNDgsIDQ4LCAxMjVd'
        self.encoded_signature = b'zoQEoijb57Fcy1LkBYzX8viTTxv9B6QGWXvC_78unIM='

        self.header = {'typ': 'JWT', 'alg': 'HS256'}
        self.payload = {'exp': 5000000000}

class JWTEncoderTestCase(JWTTestCase):

    def setUp(self):
        super().setUp()

        self.token = JWTEncoder(self.header, self.payload)

    def test_encode_header(self):
        self.assertEqual(self.token.encode_header(self.token.header), self.encoded_header)

    def test_encode_payload(self):
        self.assertEqual(self.token.encode_payload(self.token.payload), self.encoded_payload)

    def test_encode_signature(self):
        self.assertEqual(self.token.encode_signature(self.encoded_header, self.encoded_payload), self.encoded_signature)

    def test_encode_token(self):
        token = self.encoded_header + b'.' + self.encoded_payload + b'.' + self.encoded_signature
        self.assertEqual(self.token.encode_token(), token)

class JWTDecoderTestCase(JWTTestCase):

    def setUp(self):
        super().setUp()

        self.decoded_header = b'[123, 39, 116, 121, 112, 39, 58, 32, 39, 74, 87, 84, 39, 44, 32, 39, 97, 108, 103, 39, 58, 32, 39, 72, 83, 50, 53, 54, 39, 125]'
        self.decoded_payload = b'[123, 39, 101, 120, 112, 39, 58, 32, 53, 48, 48, 48, 48, 48, 48, 48, 48, 48, 125]'
        self.decoded_signature = b'\xce\x84\x04\xa2(\xdb\xe7\xb1\\\xcbR\xe4\x05\x8c\xd7\xf2\xf8\x93O\x1b\xfd\x07\xa4\x06Y{\xc2\xff\xbf.\x9c\x83'

        self.token = JWTDecoder((self.encoded_header + b'.' + self.encoded_payload + b'.' + self.encoded_signature).decode('utf-8'))

    def test_get_decoded_token(self):
        decoded_token = [self.decoded_header, self.decoded_payload, self.decoded_signature]
        self.assertEqual(self.token.get_decoded_token(), decoded_token)

    def test_get_decoded_header(self):
        self.assertEqual(self.token.get_decoded_header(), self.header)

    def test_get_decoded_payload(self):
        self.assertEqual(self.token.get_decoded_payload(), self.payload)

    def test_get_decoded_signature(self):
        self.assertEqual(self.token.get_decoded_signature(), self.decoded_signature)

    def test_compare_signatures(self):
        self.assertTrue(self.token.compare_signatures(self.header, self.payload))

    def test_is_token_expired(self):
        self.assertFalse(self.token.is_token_expired())

class UserPasswordTestCase(unittest.TestCase):
    def test_crypt_password(self):
        self.assertEqual(len(UserPassword().crypt_password('password')), 60)

    def test_compare_password(self):
        password_hash = '$2b$12$jyAgsDRKB4BuLRLEKZZqf.XUl1PmdB/xWAIFbpmEZkluDt3t6FI2m'
        self.assertTrue(UserPassword().compare_password('password', password_hash))
