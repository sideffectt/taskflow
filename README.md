# TaskFlow API

simple task management api with jwt authentication. built with fastapi and mongodb.

## how to run
```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

make sure mongodb is running first.

## auth endpoints

- `POST /auth/register` - create account
- `POST /auth/login` - get token

## task endpoints (token required)

- `POST /tasks` - create task
- `GET /tasks` - get all tasks
- `GET /tasks/{id}` - get one task
- `PUT /tasks/{id}` - update task
- `DELETE /tasks/{id}` - delete task

## example

register:
```bash
curl -X POST http://127.0.0.1:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username": "ali", "email": "ali@test.com", "password": "123456"}'
```

login:
```bash
curl -X POST http://127.0.0.1:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "ali", "password": "123456"}'
```

create task (with token):
```bash
curl -X POST http://127.0.0.1:8000/tasks \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{"title": "my task", "priority": 2}'
```

## tests
```bash
pytest tests/ -v
```

## todo

- [ ] docker support
- [ ] refresh token