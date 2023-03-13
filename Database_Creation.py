import sqlite3
conn = sqlite3.connect("Timetable2.db")
cur = conn.cursor()

#
sq1 = """
    CREATE TABLE Timetable2 (
        UniqueID TEXT,
        day TEXT,
        time1 TEXT,
        time2 TEXT,
        module_code TEXT,
        module_name TEXT,
        room TEXT,
        lecturers TEXT,
        primary key(UniqueID)
    ) """

cur.execute(sq1)
print("Timetable2 has been successfully created.")

conn.commit()
conn.close()
