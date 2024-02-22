import sqlite3
import os


db_path = os.path.join(os.path.dirname(__file__), "database.db")
conn = sqlite3.connect(db_path)
c = conn.cursor()

# Create table
c.execute(
    """CREATE TABLE if not exists factorials
             (number INTEGER, factorial INTEGER)"""
)

# Insert a row of data
c.execute("INSERT INTO factorials VALUES (0, 1)")

# Save (commit) the changes
conn.commit()

# Query the database
c.execute("SELECT * FROM factorials")
print(c.fetchall())

conn.close()
