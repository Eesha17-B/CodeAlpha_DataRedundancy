import sqlite3

def init_db():
    # Connect to database (creates data.db file if it doesn't exist)
    conn = sqlite3.connect("data.db")
    cursor = conn.cursor()

    # Create table with 4 columns
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            data_hash TEXT UNIQUE
        )
    ''')

    conn.commit()
    conn.close()
    print("Database initialized successfully!")

# Run it directly to test
if __name__ == "__main__":
    init_db()