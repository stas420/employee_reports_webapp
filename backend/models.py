
from uuid import UUID, uuid4
from datetime import datetime
from sqlite3 import Connection
import database as db

class User:
    def __init__(self, id : UUID, hash_password : str, path_to_photo : str):
        self.id = id
        self.hash_password = hash_password
        self.path_to_photo = path_to_photo

    def __str__ (self) -> str:
        return f'User: {self.id}, {self.hash_password}, {self.path_to_photo}'

    def insert_into_db(self, connection: Connection) -> bool:
        
        if db.fetch_user(connection, self.id) is not None:
            return False

        cursor = connection.cursor()
        cursor.execute('INSERT INTO users (employee_id, hash_password, path_to_photo) VALUES (?, ?, ?)', (str(self.id), self.hash_password, self.path_to_photo))
        return True
    
    def update_in_db(self, connection: Connection) -> bool:

        if db.fetch_user(connection, self.id) is None:
            return False

        cursor = connection.cursor()
        cursor.execute('UPDATE users SET hash_password = ?, path_to_photo = ? WHERE employee_id = ?', (self.hash_password, self.path_to_photo, str(self.id)))
        return True

class Timestamp:
    def __init__(self, id : UUID, employee_id : UUID, start_time : datetime, end_time : datetime, start_photo_path : str, end_photo_path : str):
        self.id = id
        self.employee_id = employee_id
        self.start_time = start_time
        self.end_time = end_time
        self.start_photo_path = start_photo_path
        self.end_photo_path = end_photo_path

    def __str__ (self) -> str:
        return f'Timestamp: {self.id}, {self.employee_id}, {self.start_time}, {self.end_time}, {self.start_photo_path}, {self.end_photo_path}'

    def insert_into_db(self, connection: Connection) -> bool:
        if db.fetch_timestamp(connection, self.id) is not None:
            return False

        cursor = connection.cursor()
        cursor.execute('INSERT INTO timestamps (entry_id, employee_id, start_time, end_time, start_photo_path, end_photo_path) VALUES (?, ?, ?, ?, ?, ?)', (str(self.id), str(self.employee_id), self.start_time.isoformat(), self.end_time.isoformat(), self.start_photo_path, self.end_photo_path))
        return True
    
