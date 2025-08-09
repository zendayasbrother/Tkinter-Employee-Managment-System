import sqlite3

def connect_database():
    try:
        sqliteConnection = sqlite3.connect('EMPLOYEE_EMS.db')
        cursor = sqliteConnection.cursor()

        # Integrity check
        cursor.execute("PRAGMA integrity_check;")
        if cursor.fetchone()[0] != "ok":
            raise sqlite3.DatabaseError("Database integrity check failed.")

        # Create Apprentices table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Employees (
                ApprenticeID INTEGER PRIMARY KEY CHECK(EmploueeID >= 5001),
                FirstName TEXT NOT NULL,
                LastName TEXT NOT NULL,
                Sex TEXT NOT NULL CHECK(Sex IN ('M', 'F')),
                DOB TEXT,
                Role TEXT NOT NULL
            )
        """)

        # Create Administrators table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Administrators (
                username TEXT PRIMARY KEY,
                password TEXT NOT NULL
            )
        """)

        # Insert default admin if not exists
        cursor.execute("INSERT OR IGNORE INTO Administrators (username, password) VALUES (?, ?)", ('zendayasbrother', '79022'))

        sqliteConnection.commit()
        return sqliteConnection, cursor

    except sqlite3.Error as error:
        print(f"Database error: {error}")
        return None, None
