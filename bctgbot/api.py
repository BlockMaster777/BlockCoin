# coding=utf-8
import hashlib
from typing import Any, Generator
from bctgbot.protocol_config import *
from bctgbot.db_manager import DatabaseManager, TokenExistsException


class InvalidTokenException(Exception):
    pass


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


def gen_data_for_hash(version: str, owner: str, randdata: str,  *_) -> str:
    return f"{version}{PART_DIVIDER}{owner}{PART_DIVIDER}{randdata}"


def split_token(token_string: str) -> tuple:
    parts = token_string.split(PART_DIVIDER)
    if len(parts) != 4:
        raise InvalidTokenException("Invalid token format")
    return parts[0], parts[1], parts[2], parts[3]


def verify_token(token: str)-> tuple[bool,  str]:
    try:
        parts = split_token(token)
    except InvalidTokenException:
        return False, "Invalid token structure"
    if parts[0] != "2.0":
        return False, "Unknown protocol version"
    if not verify_hash(gen_data_for_hash(*parts), parts[3]):
        return False, "Wrong hash"
    if not parts[3].startswith(GOAL_HASH_PREFIX):
        return False, "No goal hash prefix"
    return True,  ""


def verify_tokens(tokens: list) -> Generator[dict[str, str | bool], Any, None]:
    for i, token in enumerate(tokens):
        if token in tokens[:i]:
            yield {"result": False, "token": str(token), "err": "Duplicate token"}
            continue
        vdata = verify_token(token)
        yield {"result": vdata[0], "token": str(token), "err": vdata[1]}


def save_token(token):
    res = verify_token(token)
    if not res[0]:
        raise InvalidTokenException(res[1])
    dbm = DatabaseManager()
    dbm.insert_token(*split_token(token))


def save_tokens(tokens: list) -> int:
    wrong_count = 0
    for token in tokens:
        try:
            save_token(token)
        except InvalidTokenException, TokenExistsException:
            wrong_count += 1
            continue
    return wrong_count


def get_users_tokens(username) -> list:
    dbm = DatabaseManager()
    data = dbm.get_user_tokens(username)
    return [token[1] + PART_DIVIDER + token[2] + PART_DIVIDER + token[3] + PART_DIVIDER + token[4] for token in data]
