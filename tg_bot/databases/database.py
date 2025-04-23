import sqlite3

db: sqlite3.Connection = sqlite3.connect("databases/db.sqlite")


def add_user(id: int, last_message_id: int) -> None:
    cur = db.cursor()
    cur.execute(
        f"""INSERT INTO Users(id, last_message_id)
                    VALUES({id}, {last_message_id})""",
    )
    db.commit()


def chang_user(id: int, last_message_id: int) -> None:
    cur = db.cursor()
    cur.execute(
        f"""UPDATE Users
                    SET last_message_id = {last_message_id}
                    WHERE id == {id}""",
    )
    db.commit()


def search_user(id: int) -> bool:
    cur = db.cursor()
    result = cur.execute(
        f"""SELECT last_message_id
            FROM Users
            WHERE id == {id}"""
    ).fetchone()
    if result:
        return result[0]
