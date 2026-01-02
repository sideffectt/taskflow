# TaskFlow API

Task management REST API with JWT authentication and role-based access control.

Built with FastAPI and MongoDB.

## Features

- User registration and login (JWT)
- Role-based access control (admin/user)
- Task CRUD operations
- Profile management
- PDF export

## Quick Start
```bash
# install dependencies
pip install -r requirements.txt

# run server
uvicorn main:app --reload
```

Make sure MongoDB is running first.

## Endpoints

### Auth
- `POST /auth/register` - create account
- `POST /auth/login` - get token
- `GET /auth/profile` - view profile (token required)
- `PUT /auth/profile` - update profile (token required)

### Tasks (token required)
- `POST /tasks` - create task
- `GET /tasks` - list all tasks
- `GET /tasks/export/pdf` - download as PDF
- `GET /tasks/{id}` - get single task
- `PUT /tasks/{id}` - update task
- `DELETE /tasks/{id}` - delete task

### Admin (admin only)
- `GET /admin/users` - list all users
- `PUT /admin/users/{username}/role` - change user role

## Example

Register:
```bash
curl -X POST http://127.0.0.1:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username": "ali", "email": "ali@test.com", "password": "123456"}'
```

Login:
```bash
curl -X POST http://127.0.0.1:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "ali", "password": "123456"}'
```

Create task (with token):
```bash
curl -X POST http://127.0.0.1:8000/tasks \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{"title": "my task", "priority": 2}'
```

Export PDF:
```bash
curl -H "Authorization: Bearer YOUR_TOKEN" \
  http://127.0.0.1:8000/tasks/export/pdf \
  -o tasks.pdf
```

## Tests
```bash
pytest tests/ -v
```

## Tech Stack

- FastAPI
- MongoDB
- PyMongo
- Pydantic
- python-jose (JWT)
- reportlab (PDF)
- pytest

## Project Structure
```
taskflow/
├── main.py
├── app/
│   ├── config/      # settings, database, security, logging
│   ├── models/      # pydantic schemas
│   ├── services/    # business logic (CRUD, PDF)
│   └── routes/      # API endpoints
└── tests/
```

## TODO

- [ ] Docker support
- [ ] User-task relationship
- [ ] Pagination
- [ ] Refresh token