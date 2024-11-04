import sqlite3


def create_connection() -> sqlite3.Connection:
    return sqlite3.connect('backend/database/database.db')

def initialize_database(connection: sqlite3.Connection):
    cursor = connection.cursor()
    # Create users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            employee_id TEXT PRIMARY KEY,
            hash_password TEXT NOT NULL,
            path_to_photo TEXT NOT NULL,
            is_admin BOOLEAN DEFAULT FALSE
        );
    ''')
    # Create timestamps table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS timestamps (
            entry_id TEXT PRIMARY KEY,
            employee_id TEXT NOT NULL,
            start_time DATETIME NOT NULL,
            end_time DATETIME NOT NULL,
            start_photo_path TEXT NOT NULL,
            end_photo_path TEXT NOT NULL,
            FOREIGN KEY(employee_id) REFERENCES users(employee_id)
        );
    ''')
    connection.commit()