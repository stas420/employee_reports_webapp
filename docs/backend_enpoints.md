# API Documentation

## `POST /admin/login`

- **Description**: Admin login endpoint.
- **Request Body**:
  
  ```json
  {
    "employee_id": "string",
    "password": "string"
  }
  ```

- **Responses**:
  - `200 OK`: Returns a JWT access token.
  - `400 Bad Request`: Missing `employee_id` or `password`.
  - `404 Not Found`: User not found.
  - `403 Forbidden`: Insufficient role.
  - `401 Unauthorized`: Invalid credentials.

## `POST /user/report`

- **Description**: User report submission endpoint.
- **Request Body**:
  
  ```json
  {
    "employee_id": "string",
    "password": "string",
    "position": "string",
    "start_time": "ISO 8601 datetime",
    "end_time": "ISO 8601 datetime"
  }
  ```

- **Request Files**:
  - `start_photo`: File
  - `end_photo`: File
- **Responses**:
  - `200 OK`: Timestamp created successfully.
  - `400 Bad Request`: Missing file(s) or data in JSON body.
  - `404 Not Found`: User not found.
  - `401 Unauthorized`: Invalid credentials.
  - `409 Conflict`: Timestamp already exists.

## `GET /admin/users`

- **Description**: Get all users.
- **Responses**:
  - `200 OK`: Returns a list of users.
  - `403 Forbidden`: Insufficient role.

## `POST /admin/users`

- **Description**: Create a new user.
- **Request Body**:

  ```json
  {
    "employee_id": "string",
    "hash_password": "string",
    "path_to_photo": "string",
    "is_admin": "boolean"
  }
  ```

- **Responses**:
  - `200 OK`: User created successfully.
  - `400 Bad Request`: Missing `employee_id`, `hash_password`, or `path_to_photo`.
  - `409 Conflict`: User already exists.
  - `403 Forbidden`: Insufficient role.

## `PUT /admin/users`

- **Description**: Update an existing user.
- **Request Body**:
  
  ```json
  {
    "employee_id": "string",
    "hash_password": "string",
    "path_to_photo": "string",
    "is_admin": "boolean"
  }
  ```

- **Responses**:
  - `200 OK`: User updated successfully.
  - `400 Bad Request`: Missing `employee_id`, `hash_password`, or `path_to_photo`.
  - `404 Not Found`: User not found.
  - `403 Forbidden`: Insufficient role.

## `DELETE /admin/users`

- **Description**: Delete a user.
- **Request Body**:
  
  ```json
  {
    "employee_id": "string"
  }
  ```

- **Responses**:
  - `200 OK`: User deleted successfully.
  - `400 Bad Request`: Missing `employee_id`.
  - `404 Not Found`: User not found.
  - `403 Forbidden`: Insufficient role.

## `GET /admin/timestamps`

- **Description**: Get all timestamps or timestamps for a specific employee.
- **Query Parameters**:
  - `employee_id`: Optional, string
- **Responses**:
  - `200 OK`: Returns a list of timestamps.
  - `403 Forbidden`: Insufficient role.

## `POST /admin/timestamps/bydate`

- **Description**: Get timestamps within a date range.
- **Request Body**:
  
  ```json
  {
    "start_date": "ISO 8601 date",
    "end_date": "ISO 8601 date"
  }
  ```

- **Responses**:
  - `200 OK`: Returns a list of timestamps.
  - `400 Bad Request`: Missing or invalid date format.
  - `404 Not Found`: No timestamps found.
  - `403 Forbidden`: Insufficient role.

## `POST /admin/timestamps/report`

- **Description**: Generate a report for timestamps within a date range.
- **Request Body**:
  
  ```json
  {
    "start_date": "ISO 8601 date",
    "end_date": "ISO 8601 date"
  }
  ```

- **Responses**:
  - `200 OK`: Returns the report as an Excel file.
  - `400 Bad Request`: Missing or invalid date format.
  - `500 Internal Server Error`: Error generating report.
  - `403 Forbidden`: Insufficient role.
  