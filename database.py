import sqlite3

DB_NAME = "bot.db"


def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS favorites (
            id INTEGER PRIMARY KEY,
            user_id INTEGER,
            coin TEXT,
            UNIQUE(user_id, coin)
        )
    """)
    conn.commit()
    conn.close()


def add_favorite(user_id: int, coin: str):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT OR IGNORE INTO favorites (user_id, coin) VALUES (?, ?)",
        (user_id, coin),
    )
    conn.commit()
    conn.close()


def get_favorites(user_id: int) -> list[str]:
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT coin FROM favorites WHERE user_id = ?", (user_id,))
    rows = cursor.fetchall()
    conn.close()
    return [row[0] for row in rows]


def remove_favorite(user_id: int, coin: str):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        "DELETE FROM favorites WHERE user_id = ? AND coin = ?",
        (user_id, coin),
    )
    conn.commit()
    conn.close()