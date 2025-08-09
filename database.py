import sqlite3

def connect_database():
    try:
        sqliteConnection = sqlite3.connect('Employee EMS.db')
        cursor = sqliteConnection.cursor()

        # Create Apprentices table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Employees (
                ApprenticeID INTEGER PRIMARY KEY CHECK(EmployeesID >= 5001),
                FirstName TEXT NOT NULL,
                LastName TEXT NOT NULL,
                Sex TEXT NOT NULL CHECK(Sex IN ('M', 'F')),
                DOB DATE,
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
        cursor.execute("INSERT OR IGNORE INTO Administrators (username, password) VALUES (?, ?)", (?, ?))

        sqliteConnection.commit()
        return sqliteConnection, cursor

    except sqlite3.Error as error:
        print(f"Database error: {error}")
        return None, None
