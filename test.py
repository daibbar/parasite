import sqlite3
import pandas

conn = sqlite3.connect("./data/school_management.db")

cur = conn.cursor()


cur.execute("select * from etudiants")

rows = cur.fetchall()

for row in rows:
    print(row)