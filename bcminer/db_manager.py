# coding=utf-8
import sqlite3

class TokenExistsException(Exception):
    pass

class DatabaseManager:
    def __init__(self, db_name: str = "blockcoinminer.db") -> None:
        self.db_name = db_name
        self.create_tables()
    
    def  __execute(self, sql: str, params: tuple = ()) -> None:
        with sqlite3.connect(self.db_name) as connection:
            cursor = connection.cursor()
            cursor.execute(sql, params)
            connection.commit()
    
    def __select(self, sql: str, params: tuple = ()) -> list[tuple]:
        with sqlite3.connect(self.db_name) as connection:
            cursor = connection.cursor()
            cursor.execute(sql, params)
            return cursor.fetchall()

    def create_tables(self) -> None:
        self.__execute("""CREATE TABLE IF NOT EXISTS tokens (
                          id INTEGER PRIMARY KEY AUTOINCREMENT,
                          version TEXT NOT NULL,
                          owner TEXT NOT NULL,
                          randdata TEXT NOT NULL,
                          hash TEXT NOT NULL)""")
    
    def insert_token(self, version: str, owner: str, randdata: str, token_hash: str) -> None:
        if self.__select("SELECT * FROM tokens WHERE version = ? AND owner = ? AND randdata = ?",
                         (version ,owner, randdata)):
            raise TokenExistsException(f"Token with version '{version}' owner '{owner}' and randdata '{randdata}' "
                                       f"already exists.")
        self.__execute("INSERT INTO tokens (version, owner, randdata, hash) VALUES (?, ?, ?, ?)",
                       (version, owner, randdata, token_hash))
        
    def get_tokens(self) -> list[tuple]:
        return self.__select("SELECT * FROM tokens")
    
    def get_user_tokens(self, owner: str) -> list[tuple]:
        return self.__select("SELECT * FROM tokens WHERE owner = ?", (owner,))
