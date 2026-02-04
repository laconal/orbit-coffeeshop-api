# CoffeeShop API

A simple FastAPI application for managing a CoffeeShop backend. This project uses SQLite as the database and can be run locally or inside Docker.

### Features

- FastAPI-based REST API
- SQLite database (lightweight, file-based)
- Background tasks using Celery with Redis
- Async architecture with SQLAlchemy ORM
- Swagger UI documentation (/docs)
- Fully containerized with Docker
- Easy dependency management via requirements.txt

### Requirements

- Python > 3.12
- Docker & Docker Compose (optional)
- WSL2 (if running on Windows)

### Installation

#### Local

1. Clone repository

        git clone git@github.com:laconal/orbit-coffeeshop-api.git

        cd orbit-coffeeshop-api

2. Create virtual environemnt and activate

        python3 -m venv venv

        source venv/bin/activate # Linux / MacOS
        venv\scripts\activate # Windows

3. Install dependecies:

        pip install -r requirements.txt

4. Optional - change .env values

5. Install Redis and start

        apt install redis-server
        redis-server

6. Start FastAPI

        uvicorn app.main:app --host 0.0.0.0 --port 8000

7. Start Celery worker and beat in separate terminals:

        celery -A app.celery worker --loglevel=info
        celery -A app.celery beat --loglevel=info

8. Open Swagger UI

    ```127.0.0.1:8000/docs```

#### Docker

1.  Build image

    *If building in WSL2, install Windows Docker Desktop and enable WSL2 integration

        docker compose build

2. Start services

        docker compose up

3. Check run containers

        docker ps

4. Stop services

        docker compose down

### API


<b style="color:blue">POST</b> ```/auth/signup``` - User registration

<b style="color:blue">POST</b> ```/auth/verify``` - Verifying user via code (code prints in terminal after successfull user registration)

<b style="color:blue">POST</b> ```/auth/login``` - Getting JWT token

<b style="color:blue">POST</b> `/auth/refresh` - Refresh JWT access token

<b style="color:green">GET</b> `/me` - Get user info

<b style="color:green">GET</b> `/users` - Get all users (only for users with role Admin)

<b style="color:green">GET</b> `/users/{userID}` - Get specific information

<b style="color:purple">PATCH</b> `/users/{userID}` - Partially updates user info (only for users with role Admin)

<b style="color:red">DELETE</b> `/users/{useriD}` - Deletes user (only for users with role Admin)