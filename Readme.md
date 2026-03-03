# To-Do List API

A FastAPI-based REST API with PostgreSQL, Redis, Celery, and email notifications.

## Requirements

- Docker & Docker Compose

## Setup

1. **Clone the repository**

   ```bash
   git clone https://github.com/MaksymOleksiv/To-do-list-fastapi-test.git
   cd To-do-list-fastapi-test
   ```

2. **Create a `.env` file** in the project root:

   ```env
   POSTGRES_USER=postgres
   POSTGRES_PASSWORD=postgres
   POSTGRES_DB=todo_db
   POSTGRES_SERVER=db
   POSTGRES_PORT=5432

   REDIS_HOST=redis
   REDIS_PORT=6379

   MAIL_USERNAME=your_email@gmail.com
   MAIL_PASSWORD=your_app_password
   MAIL_FROM=your_email@gmail.com
   MAIL_PORT=587
   MAIL_SERVER=smtp.gmail.com
   MAIL_FROM_NAME=ToDo Planner

   ADMIN_EMAIL=admin@example.com
   ```

   > For Gmail, use an [App Password](https://myaccount.google.com/apppasswords) instead of your account password.

3. **Start the project**

   ```bash
   docker-compose up --build
   ```

4. **Apply database migrations**

   ```bash
   docker-compose exec app alembic upgrade head
   ```

The API will be available at `http://localhost:8000`.  
Interactive docs: `http://localhost:8000/docs`.

## Services

| Service | Description |
|---------|-------------|
| `app` | FastAPI application |
| `worker` | Celery worker (email tasks) |
| `beat` | Celery beat (scheduled cleanup of expired tasks) |
| `db` | PostgreSQL database |
| `redis` | Redis broker & cache |

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/tasks` | List all tasks |
| `GET` | `/tasks/{id}` | Get a task by ID |
| `POST` | `/tasks` | Create a new task |
| `PUT` | `/tasks/{id}` | Update a task |
| `DELETE` | `/tasks/{id}` | Delete a task |

> Rate limit: 5 requests per minute per endpoint.
