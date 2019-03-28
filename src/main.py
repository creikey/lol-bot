#!/usr/bin/env python
import coloredlogs, logging

coloredlogs.install(level="DEBUG")

import sqlite3
from sqlite3 import Error

PORT = 43522
DATABASE_FILE = "lol-bot.db"

SQL_CREATE_USERS_TABLE = """CREATE TABLE IF NOT EXISTS users (
    telegram_id integer PRIMARY KEY,
    name text NOT NULL,
    score integer
); """


def create_connection(db_file: str) -> sqlite3.Connection:
    try:
        conn = sqlite3.connect(db_file)
        logging.info(f"connected to file, sqlite version: {sqlite3.version}")
        return conn
    except Error as e:
        logging.fatal(e)
        return None


def create_table(conn: sqlite3.Connection, create_table_sql: str):
    """ Creates table from statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        logging.error(e)


def create_user(conn: sqlite3.Connection, telegram_id: int, name: str) -> int:
    """ Creates a new user from telegram id and name
    :param conn: Connection object
    :param telegram_id: a telegram user id
    :param name: a telegram name
    :return:
    """
    sql = """ INSERT INTO users(telegram_id,name,score)
    VALUES(?,?,?)"""
    cur = conn.cursor()
    cur.execute(sql, (telegram_id, name, 0))
    return cur.lastrowid


def increment_user_score(
    conn: sqlite3.Connection, telegram_id: int, increment_amount: int
):
    """ Updates score of a user by telegram id
    :param telgram_id: the user's telegram id
    :param increment_amount: amount to increment the user's score by
    :return:
    """
    sql = """ UPDATE users SET score = score + ? WHERE telegram_id = ?"""
    cur = conn.cursor()
    cur.execute(sql, (increment_amount, telegram_id))


def get_user_score(conn: sqlite3.Connection, telegram_id: int) -> int:
    """Fetches a user's score by telegram id
    :param telegram_id: the user's telegram id
    :return: returns the current score of the user
    """

    sql = """ SELECT score FROM users WHERE telegram_id = ?"""
    cur = conn.cursor()
    cur.execute(sql, [telegram_id])
    return cur.fetchone()[0]


if __name__ == "__main__":
    logging.debug(f"connecting to sqlite database file {DATABASE_FILE}...")
    conn = create_connection(DATABASE_FILE)
    if conn == None:
        exit(1)
    with conn:
        logging.debug("ensuring users table...")
        create_table(conn, SQL_CREATE_USERS_TABLE)
        # logging.debug("creating test user with id 1")
        # create_user(conn, 1, "test")
        # logging.debug(f"test user score: {get_user_score(conn, 1)}")
        # increment_user_score(conn, 0, 2)
        # logging.debug("creating test user...")
        # logging.info(f"test user id {create_user(conn, 0, 'test')}")
