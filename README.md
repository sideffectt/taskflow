# TaskFlow API

A simple task management REST API built with FastAPI and MongoDB.

## What is this?

This is my first backend project. I built it to learn how to create APIs with Python. It's a basic CRUD app where you can create, read, update and delete tasks.

## Tech Stack

- FastAPI
- MongoDB
- Pydantic
- Python 3.13

## Project Structure

```
taskflow/
├── app/
│   ├── config/         # settings, db connection, exceptions, logging
│   ├── models/         # pydantic schemas
│   ├── services/       # crud operations
│   └── api/            # routes/endpoints
├── tests/
├── main.py
└── .env
```

## Setup

1. Clone the repo

```bash
git clone https://github.com/sideffectt/taskflow.git
cd taskflow
```

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Create `.env` file (check `.env.example`)

```
MONGO_URI=mongodb://localhost:27017
DATABASE_NAME=taskflow
APP_NAME=TaskFlow API
APP_VERSION=1.0.0
DEBUG=false
```

4. Make sure MongoDB is running

```bash
brew services start mongodb-community
```

5. Run the app

```bash
uvicorn main:app --reload
```

6. Open http://127.0.0.1:8000/docs for Swagger UI

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | / | Health check |
| POST | /tasks | Create a task |
| GET | /tasks | Get all tasks |
| GET | /tasks/{id} | Get single task |
| PUT | /tasks/{id} | Update a task |
| DELETE | /tasks/{id} | Delete a task |

## Example Request

**Create a task:**

```bash
curl -X POST http://127.0.0.1:8000/tasks \
  -H "Content-Type: application/json" \
  -d '{"title": "Learn FastAPI", "priority": 3}'
```

**Response:**

```json
{
  "id": "abc123...",
  "title": "Learn FastAPI",
  "description": null,
  "completed": false,
  "priority": 3,
  "created_at": "2025-12-17T10:00:00Z",
  "updated_at": "2025-12-17T10:00:00Z"
}
```

## Running Tests

```bash
pytest tests/ -v
```

All 8 tests should pass.

## Features

- [x] CRUD operations
- [x] Input validation with Pydantic
- [x] Custom exception handling
- [x] Logging
- [ ] Authentication (maybe later)
- [ ] Docker support (maybe later)

## Notes

- Don't forget to add `.env` to `.gitignore`
- MongoDB must be running before starting the app
- Check logs in terminal for debugging

## License

None, do whatever you want with it.
