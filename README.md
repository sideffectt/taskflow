# TaskFlow API

simple task management api. my first backend project with fastapi and mongodb.

## how to run

```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

make sure mongodb is running first.

## endpoints

- `POST /tasks` - create task
- `GET /tasks` - get all tasks
- `GET /tasks/{id}` - get one task
- `PUT /tasks/{id}` - update task
- `DELETE /tasks/{id}` - delete task

## example

```bash
curl -X POST http://127.0.0.1:8000/tasks \
  -H "Content-Type: application/json" \
  -d '{"title": "my task", "priority": 2}'
```

## tests

```bash
pytest tests/ -v
```

## todo

- [ ] add authentication
- [ ] docker support
