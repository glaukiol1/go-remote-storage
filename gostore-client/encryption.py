import base64
import logging
import os
from random import SystemRandom

from cryptography.exceptions import AlreadyFinalized
from cryptography.exceptions import InvalidTag
from cryptography.exceptions import UnsupportedAlgorithm
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

# set up logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def string_encryption_password_based(plain_text, password=""):
    """
    Example for encryption and decryption of a string in one method.
    - Random password generation using strong secure random number generator
    - Random salt generation using OS random mode
    - Key derivation using PBKDF2 HMAC SHA-512
    - AES-256 authenticated encryption using GCM
    - BASE64 encoding as representation for the byte-arrays
    - UTF-8 encoding of Strings
    - Exception handling
    """
    try:
        # GENERATE password (not needed if you have a password already)
        if not password:
            alphabet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
            password = "".join(SystemRandom().choice(alphabet) for _ in range(40))
        password_bytes = password.encode('utf-8')

        # GENERATE random salt (needed for PBKDF2HMAC)
        salt = b'( \xceB\xc4\xf2$\xd8u8\n\x92\xe8\x9b^\x9dQ\x18|\xe2\x19pn\xde\x8e\xddw\xcb-\x88\xa17\xf0\xc3\xc3\xdd\xa4\x80@)\xa9\xdc\x82\nR\xc3\xef*\xf1(\xd7s\xb4L&]\xbf\xec\x0c\x16\x10\xa4p\x83'

        # DERIVE key (from password and salt)
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA512(),
            length=32,
            salt=salt,
            iterations=10000,
            backend=default_backend()
        )
        key = kdf.derive(password_bytes)

        # GENERATE random nonce (number used once)
        nonce = b'3\xca\xa0\xf2\xc3\xd2\xc1\xf3a\xaf\xa4\xdd'

        # ENCRYPTION
        aesgcm = AESGCM(key)
        cipher_text_bytes = aesgcm.encrypt(
            nonce=nonce,
            data=plain_text.encode('utf-8'),
            associated_data=None
        )
        # CONVERSION of raw bytes to BASE64 representation
        cipher_text = base64.urlsafe_b64encode(cipher_text_bytes)

        # DECRYPTION
        decrypted_cipher_text_bytes = aesgcm.decrypt(
            nonce=nonce,
            data=base64.urlsafe_b64decode(cipher_text),
            associated_data=None
        )
        # decrypted_cipher_text = decrypted_cipher_text_bytes.decode('utf-8')
        return cipher_text
    except (UnsupportedAlgorithm, AlreadyFinalized, InvalidTag):
        logger.exception("Symmetric encryption failed")

def encrypt_bytes_with_password(plain_bytes, password=""):
    """
    Example for encryption and decryption of a string in one method.
    - Random password generation using strong secure random number generator
    - Random salt generation using OS random mode
    - Key derivation using PBKDF2 HMAC SHA-512
    - AES-256 authenticated encryption using GCM
    - BASE64 encoding as representation for the byte-arrays
    - UTF-8 encoding of Strings
    - Exception handling
    """
    try:
        # GENERATE password (not needed if you have a password already)
        if not password:
            alphabet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
            password = "".join(SystemRandom().choice(alphabet) for _ in range(40))
        password_bytes = password.encode('utf-8')

        # GENERATE random salt (needed for PBKDF2HMAC)
        salt = b'( \xceB\xc4\xf2$\xd8u8\n\x92\xe8\x9b^\x9dQ\x18|\xe2\x19pn\xde\x8e\xddw\xcb-\x88\xa17\xf0\xc3\xc3\xdd\xa4\x80@)\xa9\xdc\x82\nR\xc3\xef*\xf1(\xd7s\xb4L&]\xbf\xec\x0c\x16\x10\xa4p\x83'

        # DERIVE key (from password and salt)
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA512(),
            length=32,
            salt=salt,
            iterations=10000,
            backend=default_backend()
        )
        key = kdf.derive(password_bytes)

        # GENERATE random nonce (number used once)
        nonce = b'3\xca\xa0\xf2\xc3\xd2\xc1\xf3a\xaf\xa4\xdd'

        # ENCRYPTION
        aesgcm = AESGCM(key)
        cipher_text_bytes = aesgcm.encrypt(
            nonce=nonce,
            data=plain_bytes,
            associated_data=None
        )
        # CONVERSION of raw bytes to BASE64 representation
        cipher_text = base64.urlsafe_b64encode(cipher_text_bytes)

        # DECRYPTION
        decrypted_cipher_text_bytes = aesgcm.decrypt(
            nonce=nonce,
            data=base64.urlsafe_b64decode(cipher_text),
            associated_data=None
        )
        # decrypted_cipher_text = decrypted_cipher_text_bytes.decode('utf-8')
        return cipher_text
    except (UnsupportedAlgorithm, AlreadyFinalized, InvalidTag):
        logger.exception("Symmetric encryption failed")

def decrypt_bytes(enc_bytes, password):
    try:
        # GENERATE password (not needed if you have a password already)
        if not password:
            alphabet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
            password = "".join(SystemRandom().choice(alphabet) for _ in range(40))
        password_bytes = password.encode('utf-8')

        # GENERATE random salt (needed for PBKDF2HMAC)
        salt = b'( \xceB\xc4\xf2$\xd8u8\n\x92\xe8\x9b^\x9dQ\x18|\xe2\x19pn\xde\x8e\xddw\xcb-\x88\xa17\xf0\xc3\xc3\xdd\xa4\x80@)\xa9\xdc\x82\nR\xc3\xef*\xf1(\xd7s\xb4L&]\xbf\xec\x0c\x16\x10\xa4p\x83'

        # DERIVE key (from password and salt)
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA512(),
            length=32,
            salt=salt,
            iterations=10000,
            backend=default_backend()
        )
        key = kdf.derive(password_bytes)

        # GENERATE random nonce (number used once)
        nonce = b'3\xca\xa0\xf2\xc3\xd2\xc1\xf3a\xaf\xa4\xdd'

        aesgcm = AESGCM(key)

        # DECRYPTION
        decrypted_cipher_bytes = aesgcm.decrypt(
            nonce=nonce,
            data=base64.urlsafe_b64decode(enc_bytes),
            associated_data=None
        )
        return decrypted_cipher_bytes
    except (UnsupportedAlgorithm, AlreadyFinalized, InvalidTag):
        logger.exception("Symmetric encryption failed")