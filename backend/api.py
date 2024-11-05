from flask import Flask, request, jsonify
from flask_restful import Api, Resource
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt
from uuid import uuid4
import database as db
from models import *
from dotenv import dotenv_values
import bcrypt
import datetime as dt
from datetime import datetime
from report import Report
from io import BytesIO
import ipaddress
from functools import wraps
import os

config = dotenv_values()
if not config or not config.get('JWT_SECRET_KEY') or not config.get('IP_WHITELIST'):
    raise ValueError('Missing JWT_SECRET_KEY or IP_WHITELIST in .env file')
app = Flask(__name__)
api = Api(app)
app.config['JWT_SECRET_KEY'] = config['JWT_SECRET_KEY']
jwt = JWTManager(app)

IP_RANGE = ipaddress.ip_network(config['IP_WHITELIST'] or '0.0.0.0/0')

UPLOAD_FOLDER = 'backend/photos'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def role_required(role):
    def wrapper(fn):
        @jwt_required()
        def decorator(*args, **kwargs):
            claims = get_jwt()
            if claims['role'] != role:
                return jsonify(message='Access forbidden: Insufficient role'), 403
            return fn(*args, **kwargs)
        return decorator
    return wrapper

def ip_required(allowed_ip_network: ipaddress.IPv4Network | ipaddress.IPv6Network):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            client_ip_str = request.remote_addr
            if not client_ip_str:
                return jsonify(message='Client IP not found'), 400
            client_ip : ipaddress.IPv4Address | ipaddress.IPv6Address = ipaddress.ip_address(client_ip_str)
            if client_ip not in allowed_ip_network:
                return jsonify(message='Access forbidden: Invalid IP'), 403
        return wrapper
    return decorator

@ip_required(IP_RANGE)
@app.route('/admin/login', methods=['POST'])
def admin_login():
    data = request.get_json()
    if 'employee_id' not in data or 'password' not in data:
        return jsonify(message='Missing employee_id or password'), 400
    connection = db.create_connection()
    user: User | None = User.fetch_from_db(data['employee_id'], connection)
    if not user:
        return jsonify(message='User not found'), 404
    connection.close()
    if not user.is_admin:
        return jsonify(message='Access forbidden: Insufficient role'), 403
    if user and bcrypt.checkpw(data['password'].encode(), user.hash_password.encode()):
        access_token = create_access_token(identity=user.id, additional_claims={"role": "admin"})
        return jsonify(access_token=access_token)
    return jsonify(message='Invalid credentials'), 401

@ip_required(IP_RANGE)
@app.route('/user/report', methods=['POST'])
def user_report():
    if 'start_photo' not in request.files or 'end_photo' not in request.files:
        return jsonify(message='Missing file(s)'), 400
    
    start_photo = request.files['start_photo']
    end_photo = request.files['end_photo']

    if start_photo.filename == '' or end_photo.filename == '':
        return jsonify(message='No selected file(s)'), 400

    timestamp_id = uuid4()

    start_photo_path = os.path.join(UPLOAD_FOLDER, f"{timestamp_id}_{start_photo.filename}")
    end_photo_path = os.path.join(UPLOAD_FOLDER, f"{timestamp_id}_{end_photo.filename}")

    start_photo.save(start_photo_path)
    end_photo.save(end_photo_path)

    data = request.get_json()
    
    if all(key in data for key in ['employee_id', 'password', 'position', 'start_time', 'end_time']):
        return jsonify(message="Missing data in json body"), 400

    connection = db.create_connection()  # Create a new connection for each request
    try:
        user = User.fetch_from_db(data['employee_id'], connection)
        if not user:
            return jsonify(message='User not found'), 404
        if not user.authenticate(data['password']):
            return jsonify(message='Invalid credentials'), 401
        timestamp = Timestamp(
            timestamp_id,
            user.id, 
            data['position'],
            datetime.fromisoformat(data['start_time']), 
            datetime.fromisoformat(data['start_time']), 
            start_photo_path, 
            end_photo_path
        )

        if timestamp.insert_into_db(connection):
            connection.commit()
            return jsonify(message='Timestamp created successfully')
        return jsonify(message='Timestamp already exists'), 409
    finally:
        connection.close()  # Ensure the connection is closed after the request

@ip_required(IP_RANGE)
@role_required('admin')
@app.route('/admin/users', methods=['GET'])
def admin_get_users():
    connection = db.create_connection()
    users = User.fetch_all_from_db(connection)
    connection.close()
    return jsonify(users=[user.to_dict() for user in users])

@ip_required(IP_RANGE)
@role_required('admin')
@app.route('/admin/users', methods=['POST'])
def admin_create_user():
    data = request.get_json()
    if not all(key in data for key in ['employee_id', 'hash_password', 'path_to_photo']):
        return jsonify(message='Missing employee_id, hash_password or path_to_photo'), 400
    connection = db.create_connection()
    try:
        user = User(data['employee_id'], bcrypt.hashpw(data['hash_password'].encode(), bcrypt.gensalt()).decode(), data['path_to_photo'], data.get('is_admin', False))
        if user.insert_into_db(connection):
            connection.commit()
            return jsonify(message='User created successfully')
        return jsonify(message='User already exists'), 409
    finally:
        connection.close()

@ip_required(IP_RANGE)
@role_required('admin')
@app.route('/admin/users', methods=['PUT'])
def admin_update_user():
    data = request.get_json()
    if not all(key in data for key in ['employee_id', 'hash_password', 'path_to_photo']):
        return jsonify(message='Missing employee_id, hash_password or path_to_photo'), 400
    connection = db.create_connection()
    try:
        user = User(data['employee_id'], bcrypt.hashpw(data['hash_password'].encode(), bcrypt.gensalt()).decode(), data['path_to_photo'], data.get('is_admin', False))
        if user.update_in_db(connection):
            connection.commit()
            return jsonify(message='User updated successfully')
        return jsonify(message='User not found'), 404
    finally:
        connection.close()

@ip_required(IP_RANGE)
@role_required('admin')
@app.route('/admin/users', methods=['DELETE'])
def admin_delete_user():
    data = request.get_json()
    if 'employee_id' not in data:
        return jsonify(message='Missing employee_id'), 400
    connection = db.create_connection()
    try:
        user = User(data['employee_id'], '', '', False)
        if user.delete_from_db(connection):
            connection.commit()
            return jsonify(message='User deleted successfully')
        return jsonify(message='User not found'), 404
    finally:
        connection.close()

@ip_required(IP_RANGE)
@role_required('admin')
@app.route('/admin/timestamps', methods=['GET'])
def admin_get_timestamps():
    connection = db.create_connection()
    if id := request.args.get('employee_id'):
        timestamps = Timestamp.fetch_all_for_employee(id, connection)
    else:
        timestamps = Timestamp.fetch_all_from_db(connection)
    connection.close()
    return jsonify(timestamps=[timestamp.to_dict() for timestamp in timestamps])

@ip_required(IP_RANGE)
@role_required('admin')
@app.route('/admin/timestamps/bydate', methods=['POST'])
def admin_get_timestamps_by_date():
    data = request.get_json()
    if not all(key in data for key in ['start_date', 'end_date']):
        return jsonify(message='Missing start_date or end_date'), 400
    try:
        start_date = datetime.fromisoformat(data['start_date'])
        end_date = datetime.fromisoformat(data['end_date'])

        if start_date > end_date:
            raise ValueError('start_date cannot be greater than end_date')
    except ValueError:
        return jsonify(message='Invalid date format'), 400
    
    connection = db.create_connection()
    filter_func = lambda timestamp: timestamp.start_time >= start_date and timestamp.start_time <= end_date
    timestamps = Timestamp.fetch_all_if(filter_func, connection)
    connection.close()
    if not timestamps:
        return jsonify(message='No timestamps found'), 404
    return jsonify(timestamps=[timestamp.to_dict() for timestamp in timestamps])

@ip_required(IP_RANGE)
@role_required('admin')
@app.route('/admin/timestamps/report', methods=['POST'])
def admin_get_report():
    data = request.get_json()
    if not all(key in data for key in ['start_date', 'end_date']):
        return jsonify(message='Missing start_date or end_date'), 400
    try:
        start_date = datetime.fromisoformat(data['start_date'])
        end_date = datetime.fromisoformat(data['end_date'])

        if start_date > end_date:
            raise ValueError('start_date cannot be greater than end_date')
    except ValueError:
        return jsonify(message='Invalid date format'), 400
    
    connection = db.create_connection()
    timestamps = Timestamp.fetch_all_for_duration(start_date, end_date, connection)
    connection.close()
    report = Report(timestamps)
    wb = report.generate_report()
    if not wb:
        return jsonify(message='Error generating report'), 500
    output_bytes = BytesIO()
    wb.save(output_bytes)
    output_bytes.seek(0)

    return output_bytes, 200, {'Content-Type': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', 'Content-Disposition': 'attachment; filename=report.xlsx'}



if __name__ == '__main__':
    app.run(debug=True)