import sqlite3
from models import User, Timestamp
import bcrypt as bc


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
            position TEXT NOT NULL,
            start_time DATETIME NOT NULL,
            end_time DATETIME,
            start_photo_path TEXT NOT NULL,
            end_photo_path TEXT,
            FOREIGN KEY(employee_id) REFERENCES users(employee_id)
        );
    ''')
    connection.commit()

if __name__ == '__main__':
    connection = create_connection()
    initialize_database(connection)
    salt = bc.gensalt()
    pw_hash = str(bc.hashpw('password'.encode(), salt))
    print(pw_hash)
    user = User('example_user_2137', pw_hash, 'path/to/photo', True)
    user.insert_into_db(connection)
    connection.commit()
    connection.close()