# FastAPI Task API with JWT Authentication

A simple REST API for task management with JWT-based authentication.

## Features

- User registration and login (supports both form and JSON)
- JWT token-based authentication
- Protected task management endpoints
- Comprehensive API documentation

## Project Structure

```
fastapi/
├── auth/                 # Authentication-related code
│   ├── __init__.py
│   ├── jwt_bearer.py     # JWT token validation
│   ├── jwt_handler.py    # JWT token generation and decoding
│   └── users.py          # User authentication functions
├── db/                   # Data models and storage
│   ├── task.py           # Task model and in-memory storage
│   └── user.py           # User model and in-memory storage
├── main.py               # FastAPI application and endpoints
├── requirements.txt      # Project dependencies
└── README.md             # This documentation
```

## Installation

1. Clone the repository
2. Create a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Run the server:
   ```
   python main.py
   ```

## API Endpoints

### Authentication

- **POST /register** - Register a new user
  - Request body: `{ "email": "user@example.com", "username": "username", "password": "password" }`

- **POST /login** - Login with form data and get access token
  - Form data: `username` and `password`
  - Returns: JSON Web Token to be used in subsequent requests

- **POST /login-json** - Login with JSON and get access token
  - Request body: `{ "username": "username", "password": "password" }`
  - Returns: JSON Web Token to be used in subsequent requests

### Tasks (Protected Routes)

All task endpoints require authentication using a JWT token. Include the token in the Authorization header:
```
Authorization: Bearer your-jwt-token
```

- **GET /tasks** - Get all tasks
- **GET /tasks/{task_id}** - Get task by ID
- **POST /tasks** - Create a new task
- **PUT /tasks/{task_id}** - Update a task
- **DELETE /tasks/{task_id}** - Delete a task

## Authentication Flow

1. Register a new user account via `/register`
2. Login with username and password via `/login` or `/login-json`
3. Store the returned JWT token
4. Include the token in the `Authorization` header for all protected routes

## API Documentation

FastAPI automatically generates interactive API documentation:

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Security Notes

For production use, consider making these improvements:

1. Store JWT secret key in environment variables
2. Implement refresh tokens
3. Use a real database (PostgreSQL, MongoDB, etc.)
4. Add more user validation (email verification, password strength, etc.)
5. Consider implementing rate limiting