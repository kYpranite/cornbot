import sqlite3

conn = sqlite3.connect('options.db')
cursor = conn.cursor()
def deleteDuplicates():
    with conn:
        cursor.execute("CREATE TABLE temp_table as SELECT DISTINCT * FROM options")
        cursor.execute("DELETE FROM options")
        cursor.execute("INSERT INTO options SELECT * FROM temp_table")

print("executing")
deleteDuplicates()
