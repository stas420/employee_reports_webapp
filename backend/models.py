from uuid import UUID, uuid4
from datetime import datetime
from sqlite3 import Connection
from abc import ABC, abstractmethod
from typing import Optional, Sequence, Callable
import bcrypt as bc

class Model(ABC):
    @staticmethod
    @abstractmethod
    def from_row(row) -> 'Model':
        pass

    @staticmethod
    @abstractmethod
    def fetch_from_db(id, connection: Connection) -> Optional['Model']:
        pass
    @staticmethod
    @abstractmethod
    def fetch_all_from_db(connection: Connection) -> Sequence['Model']:
        pass
    @abstractmethod
    def insert_into_db(self, connection: Connection) -> bool:
        pass
    @abstractmethod
    def update_in_db(self, connection: Connection) -> bool:
        pass
    @abstractmethod
    def delete_from_db(self, connection: Connection) -> bool:
        pass
    @abstractmethod
    def to_dict(self) -> dict:
        pass
    



class User(Model):
    def __init__(self, id : str, hash_password : str, path_to_photo : str, is_admin : bool):
        self.id : str = id
        self.hash_password : str = hash_password
        self.path_to_photo : str = path_to_photo
        self.is_admin : bool = is_admin

    @staticmethod
    def from_row(row) -> 'User':
        return User(str(row[0]), str(row[1]), str(row[2]), bool(row[3]))
    
    @staticmethod
    def fetch_from_db(id, connection : Connection) -> Optional['User']:
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM users WHERE employee_id = ?, (id,))')
        row = cursor.fetchone()
        if row:
            return User.from_row(row)
        return None
    
    @staticmethod
    def fetch_all_from_db(connection : Connection) -> Sequence['User']:
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM users')
        return [User.from_row(row) for row in cursor.fetchall()]
    
    def insert_into_db(self, connection : Connection) -> bool:
        cursor = connection.cursor()
        cursor.execute('INSERT INTO users VALUES (?, ?, ?, ?)', (self.id, self.hash_password, self.path_to_photo, self.is_admin))
        return cursor.rowcount == 1
    def update_in_db(self, connection : Connection) -> bool:
        cursor = connection.cursor()
        cursor.execute('UPDATE users SET hash_password = ?, path_to_photo = ?, is_admin = ? WHERE employee_id = ?', (self.hash_password, self.path_to_photo, self.is_admin, self.id))
        return cursor.rowcount == 1
    def delete_from_db(self, connection : Connection) -> bool:
        cursor = connection.cursor()
        cursor.execute('DELETE FROM users WHERE employee_id = ?', (self.id,))
        return cursor.rowcount == 1
    def to_dict(self) -> dict:
        return {
            'employee_id': self.id,
            'hash_password': self.hash_password,
            'path_to_photo': self.path_to_photo,
            'is_admin': self.is_admin
        }
    def authenticate(self,password : str) -> bool:
        return bc.checkpw(password.encode(), self.hash_password.encode())
    

class Timestamp(Model):
    def __init__(self, id : UUID, employee_id : str, position : str, start_time : datetime, end_time : datetime, start_photo_path : str, end_photo_path : str):
        self.id = id
        self.employee_id = employee_id
        self.position = position
        self.start_time = start_time
        self.end_time = end_time
        self.start_photo_path = start_photo_path
        self.end_photo_path = end_photo_path

    @staticmethod
    def from_row(row) -> 'Timestamp':
        return Timestamp(UUID(row[0]), str(row[1]), str(row[2]), datetime.fromisoformat(row[3]), datetime.fromisoformat(row[4]), str(row[5]), str(row[6]))

    @staticmethod
    def fetch_from_db(id, connection : Connection) -> Optional['Timestamp']:
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM timestamps WHERE entry_id = ?', (id,))
        row = cursor.fetchone()
        if row:
            return Timestamp.from_row(row)
        return None
    
    @staticmethod
    def fetch_all_from_db(connection : Connection) -> Sequence['Timestamp']:
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM timestamps')
        return [Timestamp.from_row(row) for row in cursor.fetchall()]
    
    @staticmethod
    def fetch_all_for_employee(employee_id : str, connection : Connection) -> Sequence['Timestamp']:
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM timestamps WHERE employee_id = ?', (employee_id,))
        return [Timestamp.from_row(row) for row in cursor.fetchall()]
    
    @staticmethod
    def fetch_all_for_duration(start_time : datetime, end_time : datetime, connection : Connection) -> Sequence['Timestamp']:
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM timestamps WHERE start_time >= ? AND end_time <= ?', (start_time.isoformat(), end_time.isoformat()))
        return [Timestamp.from_row(row) for row in cursor.fetchall()]

    @staticmethod
    def fetch_all_if(filter_func: Callable[['Timestamp'], bool], connection : Connection) -> Optional[Sequence['Timestamp']]:
        timestamps = Timestamp.fetch_all_from_db(connection)
        filtered = list(filter(filter_func, timestamps))
        return filtered if filtered else None
    
    def insert_into_db(self, connection : Connection) -> bool:
        cursor = connection.cursor()
        cursor.execute('INSERT INTO timestamps VALUES (?, ?, ?, ?, ?, ?, ?)', (self.id, self.employee_id, self.position, self.start_time.isoformat(), self.end_time.isoformat(), self.start_photo_path, self.end_photo_path))
        return cursor.rowcount == 1
    
    def update_in_db(self, connection : Connection) -> bool:
        cursor = connection.cursor()
        cursor.execute('UPDATE timestamps SET employee_id = ?, position = ?, start_time = ?, end_time = ?, start_photo_path = ?, end_photo_path = ? WHERE entry_id = ?', (self.employee_id, self.position, self.start_time.isoformat(), self.end_time.isoformat(), self.start_photo_path, self.end_photo_path, self.id))
        return cursor.rowcount == 1
    
    def delete_from_db(self, connection : Connection) -> bool:
        cursor = connection.cursor()
        cursor.execute('DELETE FROM timestamps WHERE entry_id = ?', (self.id,))
        return cursor.rowcount == 1
    
    def to_dict(self) -> dict:
        return {
            'entry_id': self.id,
            'employee_id': self.employee_id,
            'start_time': self.start_time.isoformat(),
            'end_time': self.end_time.isoformat(),
            'start_photo_path': self.start_photo_path,
            'end_photo_path': self.end_photo_path
        }
    

