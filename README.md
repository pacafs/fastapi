# FastAPI Task API with JWT Authentication

A simple REST API for task management with JWT-based authentication.

## Features

- User registration and login (supports both form and JSON)
- JWT token-based authentication
- Protected task management endpoints
- Comprehensive API documentation
- Environment-based configuration

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
├── .env                  # Environment variables (not committed to version control)
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

4. Create a `.env` file with your environment variables or use the provided example:
   ```
   # JWT Configuration
   JWT_SECRET="your_generated_secret_key"
   JWT_ALGORITHM="HS256"
   ACCESS_TOKEN_EXPIRE_MINUTES=30

   # Application Settings
   APP_NAME="Task Management API" 
   APP_VERSION="1.0.0"
   DEBUG=True

   # API Settings
   HOST="0.0.0.0"
   PORT=8000
   ```

5. Run the server:
   ```
   python main.py
   ```

## Environment Variables

| Variable                  | Description                              | Default                       |
|---------------------------|------------------------------------------|-------------------------------|
| JWT_SECRET                | Secret key for JWT token signature       | (fallback development secret) |
| JWT_ALGORITHM             | Algorithm for JWT token encryption       | HS256                         |
| ACCESS_TOKEN_EXPIRE_MINUTES | Token expiration time in minutes       | 30                            |
| APP_NAME                  | Name of the application                  | Task Management API           |
| APP_VERSION               | Version of the application               | 1.0.0                         |
| DEBUG                     | Enable debug mode (auto-reload)          | False                         |
| HOST                      | Server host                              | 0.0.0.0                       |
| PORT                      | Server port                              | 8000                          |

For security, it's recommended to generate a random JWT_SECRET using Python:
```python
import secrets
print(secrets.token_hex(32))
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