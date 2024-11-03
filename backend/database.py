import sqlite3
from models import *
from typing import Optional
import hashlib as hasher

def create_connection() -> sqlite3.Connection:
    return sqlite3.connect('backend/database/database.db')

def initialize_database(connection: sqlite3.Connection):
    cursor = connection.cursor()
    # Create users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            employee_id TEXT PRIMARY KEY,
            hash_password TEXT NOT NULL,
            path_to_photo TEXT NOT NULL
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

def fetch_user(connection: sqlite3.Connection, employee_id: str) -> Optional['User']:
    cursor = connection.cursor()
    cursor.execute('SELECT employee_id, hash_password, path_to_photo FROM users WHERE employee_id = ?', (employee_id,))
    row = cursor.fetchone()
    if row:
        return User(row[0], row[1], row[2])
    return None

def fetch_timestamp(connection: sqlite3.Connection, entry_id: str) -> Optional['Timestamp']:
    cursor = connection.cursor()
    cursor.execute('SELECT entry_id, employee_id, start_time, end_time, start_photo_path, end_photo_path FROM timestamps WHERE entry_id = ?', (str(entry_id),))
    row = cursor.fetchone()
    if row:
        return Timestamp(UUID(row[0]), row[1], datetime.fromisoformat(row[2]), datetime.fromisoformat(row[3]), row[4], row[5])
    return None

if __name__ == '__main__':
    connection = create_connection()
    initialize_database(connection)
    
    user = User('example_user_2137', hasher.sha256('password'.encode()).hexdigest(), 'example/path')
    print(user)
    user.insert_into_db(connection)
    read_user = fetch_user(connection, user.id)
    print(read_user)

    timestamp = Timestamp(uuid4(), user.id, datetime.now(), datetime.now(), 'example/path', 'example/path')
    print(timestamp)
    timestamp.insert_into_db(connection)
    read_timestamp = fetch_timestamp(connection, timestamp.id)
    print(read_timestamp)
    connection.rollback()
    connection.close()