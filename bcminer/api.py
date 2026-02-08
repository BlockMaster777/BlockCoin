# coding=utf-8
import hashlib
import random
from collections.abc import Callable

from bcminer.protocol_config import *
from bcminer.db_manager import DatabaseManager


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
        
        def get_tuple(self) -> tuple:
            """Return the token data as a tuple."""
            return self.version, self.owner, self.randdata, self.token_hash


def remove_id_from_token_tuple(token_tuple: tuple) -> tuple:
    """Remove the ID from the token tuple for comparison purposes."""
    return token_tuple[1:]

def null():
    pass


class Generator:
    def __init__(self, update_function: Callable = null) -> None:
        self.dbm = DatabaseManager()
        self.update_function = update_function
        self.valid_tokens = set(remove_id_from_token_tuple(tok_tuple) for tok_tuple in self.dbm.get_tokens())
    
    @staticmethod
    def generate_token(owner: str) -> Token:
        """Generate a new token for the specified owner."""
        randdata = generate_random_data()
        token_string = gen_data_for_hash(VERSION, owner, randdata)
        token_hash = hash_data(token_string)
        token = Token(VERSION, owner, randdata, token_hash)
        return token
    
    def generate_one_valid_token(self, owner: str) -> Token:
        """Generate a valid token that meets the goal hash prefix requirement."""
        while True:
            token = self.generate_token(owner)
            if token.token_hash.startswith(GOAL_HASH_PREFIX):
                if not token.get_tuple() in self.valid_tokens:
                    self.valid_tokens.add(token.get_tuple())
                    self.dbm.insert_token(token.version, token.owner, token.randdata, token.token_hash)
                return token
    
    def generate_valid_tokens(self, owner: str, count: int) -> list[Token]:
        """Generate a specified number of valid tokens for the given owner."""
        tokens = []
        for _ in range(count):
            token = self.generate_one_valid_token(owner)
            tokens.append(token)
            self.update_function()
        return tokens


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


if __name__ == '__main__':
    generator = Generator()
    print(generator.generate_valid_tokens(owner="Alice", count=5))
