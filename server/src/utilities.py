# -*- coding: utf-8 -*-

import ast
import time
import crypt
from hashlib import sha256
from base64 import urlsafe_b64encode, urlsafe_b64decode
from hmac import compare_digest

class JWTEncoder():
    "Encodes the JWT."

    header = None
    payload = None

    def __init__(self, header = {}, payload = {}):
        self.header = header
        self.payload = payload

    def encode_part(self, dictionary):
        "Encodes a token part to the array of bytes."
        return str(list(str(dictionary).encode('utf-8'))).encode('utf-8')

    def encode_header(self, header):
        "Encodes the header to the base64url-encoded value."
        encoded_header = self.encode_part(header)
        b64encoded_header = urlsafe_b64encode(encoded_header)
        return b64encoded_header

    def encode_payload(self, payload):
        "Encodes the payload to the base64url-encoded value."
        encoded_payload = self.encode_part(payload)
        b64encoded_payload = urlsafe_b64encode(encoded_payload)
        return b64encoded_payload

    def encode_signature(self, encoded_header, encoded_payload):
        "Encodes the signature hash to the base64url-encoded value."
        signature_hash = sha256(encoded_header + b'.' + encoded_payload).digest()
        b64encoded_signature = urlsafe_b64encode(signature_hash)
        return b64encoded_signature

    def encode_token(self):
        "Encodes the complete token."
        encoded_header = self.encode_header(self.header)
        encoded_payload = self.encode_payload(self.payload)
        encoded_signature = self.encode_signature(encoded_header, encoded_payload)
        token = encoded_header  + b'.' + encoded_payload + b'.' + encoded_signature
        return token

class JWTDecoder():
    "Decodes the JWT."

    token = None

    def __init__(self, token = None):
        self.token = token

    def get_decoded_token(self):
        "Decodes the complete token from the base64url-encoded value."
        splitted_token = self.token.split('.')
        decoded_header = urlsafe_b64decode(splitted_token[0])
        decoded_payload = urlsafe_b64decode(splitted_token[1])
        decoded_signature = urlsafe_b64decode(splitted_token[2])
        return [decoded_header, decoded_payload, decoded_signature]

    def decode_part(self, part):
        "Decodes a token part from the array of bytes."
        return ast.literal_eval(bytearray(ast.literal_eval(part.decode('utf-8'))).decode('utf-8'))

    def get_decoded_header(self):
        "Decodes the header."
        decoded_token = self.get_decoded_token()
        decoded_header = self.decode_part(decoded_token[0])
        return decoded_header

    def get_decoded_payload(self):
        "Decodes the payload."
        decoded_token = self.get_decoded_token()
        decoded_payload = self.decode_part(decoded_token[1])
        return decoded_payload

    def get_decoded_signature(self):
        "Decodes the signature hash."
        decoded_token = self.get_decoded_token()
        return decoded_token[2]

    def compare_signatures(self, compared_header, compared_payload):
        "Compares the a custom signature with the signature hash."
        encoded_header = JWTEncoder().encode_header(compared_header)
        encoded_payload = JWTEncoder().encode_payload(compared_payload)
        signature_hash = sha256(encoded_header + b'.' + encoded_payload).digest()

        return compare_digest(self.get_decoded_signature(), signature_hash)

    def is_token_expired(self):
        "Checks the expiration time."
        decoded_payload = self.get_decoded_payload()
        return round(time.time()) > decoded_payload['exp']

class UserPassword:
    "The utility for the user password."

    def crypt_password(self, password):
        "Crypts a password."
        password_hash = crypt.crypt(password, crypt.METHOD_BLOWFISH)
        return password_hash

    def compare_password(self, password, password_hash):
        "Compares a custom password with the password hash."
        return compare_digest(password_hash, crypt.crypt(password, password_hash))
