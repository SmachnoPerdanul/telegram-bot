import sqlite3

conn = sqlite3.connect("bot.db")
cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS favorites (
        id INTEGER PRIMARY KEY,
        user_id INTEGER,
        coin TEXT,
        UNIQUE(user_id, coin)
    )
""")

cursor.execute("INSERT OR IGNORE INTO favorites (user_id, coin) VALUES (?, ?)", (12345, "bitcoin"))
cursor.execute("INSERT OR IGNORE INTO favorites (user_id, coin) VALUES (?, ?)", (12345, "ethereum"))

conn.commit()

cursor.execute("SELECT coin FROM favorites WHERE user_id = ?", (12345,))
rows = cursor.fetchall()
print("Сырой результат:", rows)

coins = [row[0] for row in rows]
print("Монеты пользователя:", coins)

conn.close()