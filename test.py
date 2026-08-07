import sqlite3

conn = sqlite3.connect("db/booking.db")
cursor = conn.cursor()

cursor.execute("SELECT * FROM booking_info")

for row in cursor.fetchall():
    print(row)

conn.close()