from flask import Flask, request, jsonify
from flask_restful import Api, Resource
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity, get_jwt
from uuid import uuid4
import database as db
import models
from dotenv import dotenv_values
import bcrypt
import datetime as dt
from datetime import datetime

config = dotenv_values()
app = Flask(__name__)
api = Api(app)
app.config['JWT_SECRET_KEY'] = config['JWT_SECRET_KEY']
jwt = JWTManager(app)

connection = db.create_connection()
db.initialize_database(connection)

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

@app.route('/user/login', methods=['POST'])
def user_login():
    data = request.get_json()
    user = db.fetch_user(db.create_connection(), data['employee_id'])
    if user and bcrypt.checkpw(data['password'].encode(), user.hash_password):
        access_token = create_access_token(identity=user.id, additional_claims={"role": "employee"})
        return jsonify(access_token=access_token)
    return jsonify(message='Invalid credentials'), 401

@app.route('/admin/login', methods=['POST'])
def admin_login():
    data = request.get_json()
    user = db.fetch_user(db.create_connection(), data['employee_id'])
    if not user.is_admin:
        return jsonify(message='Access forbidden: Insufficient role'), 403
    if user and bcrypt.checkpw(data['password'].encode(), user.hash_password):
        access_token = create_access_token(identity=user.id, additional_claims={"role": "admin"})
        return jsonify(access_token=access_token)
    return jsonify(message='Invalid credentials'), 401

@app.route('/user/report', methods=['POST'])
@role_required('employee')
def user_report():
    data = request.get_json()
    connection = db.create_connection()  # Create a new connection for each request
    try:
        user = db.fetch_user(connection, get_jwt_identity())
        timestamp = models.Timestamp(uuid4(), user.id, datetime.fromisoformat(data['start_time']), datetime.fromisoformat(data['end_time']), data['start_photo_path'], data['end_photo_path'])

        if timestamp.insert_into_db(connection):
            connection.commit()
            return jsonify(message='Timestamp created successfully')
        return jsonify(message='Timestamp already exists'), 409
    finally:
        connection.close()  # Ensure the connection is closed after the request


if __name__ == '__main__':
    app.run(debug=True)