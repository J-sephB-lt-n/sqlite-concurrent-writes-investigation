
import sqlite3

sql = sqlite3.connect("database.db")

sql.execute("CREATE TABLE games (release_year INTEGER, name TEXT, genre TEXT);")

sql.close()
