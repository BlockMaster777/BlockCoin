# coding=utf-8
import hashlib
import random
from protocol_config import *


class InvalidTokenException(Exception):
    pass


class Token:
        def __init__(self, version: str, owner: str, randdata: str, token_hash: str) -> None:
            self.version = version
            self.owner = owner
            self.randdata = randdata
            self.token_hash = token_hash
        
        @classmethod
        def from_token_string(cls, token_string: str) -> Token:
            parts = token_string.split(PART_DIVIDER)
            if len(parts) != 4:
                raise InvalidTokenException("Invalid token format")
            return cls(parts[0], parts[1], parts[2], parts[3])
        
        def __str__(self) -> str:
            """Format the token as a string using the defined format."""
            return f"{self.version}{PART_DIVIDER}{self.owner}{PART_DIVIDER}{self.randdata}{PART_DIVIDER}{self.token_hash}"


def hash_data(data: str) -> str:
    """Hash the input data using SHA-256 and return the hexadecimal representation."""
    sha256_hash = hashlib.sha256()
    sha256_hash.update(data.encode())
    sha256_hash.update(sha256_hash.hexdigest().encode())
    sha256_hash.update(bytes(SALT.encode()))
    return sha256_hash.hexdigest()


def verify_hash(data: str, expected_hash: str) -> bool:
    """Verify that the hash of the input data matches the expected hash."""
    return hash_data(data) == expected_hash


def generate_random_data() -> str:
    """Generate a random string of the specified length."""
    characters = RANDOM_CHARS
    return ''.join(random.choice(characters) for _ in range(RANDOM_CHARS_LEN))


def gen_data_for_hash(version: str, owner: str, randdata: str) -> str:
    return f"{version}{PART_DIVIDER}{owner}{PART_DIVIDER}{randdata}"
