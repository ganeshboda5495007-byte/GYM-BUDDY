import sqlite3

conn = sqlite3.connect("ai_gym_fitness.db")
conn.execute("ALTER TABLE users ADD COLUMN is_admin INTEGER DEFAULT 0")
conn.commit()
conn.close()
print("Column added!")
