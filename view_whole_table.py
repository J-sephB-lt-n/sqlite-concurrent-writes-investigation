
import sqlite3

sql = sqlite3.connect("database.db")
sql_cursor = sql.cursor()
sql_cursor.execute("SELECT * FROM games;")
print("(release_year, name, genre)")
for row in sql_cursor.fetchall():
    print(row)
sql.close()
