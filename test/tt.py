import sqlite3 as sq


file = "test.db"
try : 
    conn = sq.connect(file)
    print("success")
except:
    print("Error")

conn.close()