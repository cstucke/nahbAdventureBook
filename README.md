# nahbAdventureBook

A full-stack web application for creating, playing, and managing interactive, branching text adventures.

## Architecture
This project is built using a decoupled microservice architecture:

Flask API: The core data engine. It manages the creation, storage, and retrieval of Stories, Pages, and Choices using a SQLite database (instance/app.db). It processes probability-based random events and is protected via an API key.

Django Application: The user-facing client. It handles user authentication, session tracking, gameplay execution, reviews, and moderation reporting. The interface provides seamless navigation across a personal page for individual story management, a community feed for updates, and a global page to discover all available modules.

## Prerequisites
- Python 3.12
- pip
- virtualenv

## Setup Instructions
1. Environment Preparation
Create and activate a virtual environment in the root directory
```bash
python3.12 -m venv venv
source venv/bin/activate
pip install -r flask_api/requirements.txt -r django_app/requirements.txt
```

2. Config
Ensure a .env file exists in the root directory that matches the .env.example layout.

3. Database Initalization
Flask:
```bash
cd flask_api
flask db upgrade
cd ..
```

Django:
```bash
cd django_app
python manage.py migrate
python manage.py createsuperuser
cd ..
```

## Run Instructions

In order to run this app, you must have two separate terminal windows open to run both servers.

Terminal 1:
```bash
cd flask_api
flask run --port=5000
```

Terminal 2:
```bash
cd django_app
python manage.py runserver 8000
```

As before, you must establish a superuser and any other users you wish to use after generating the databases for both the flask api and django applications.

## Flask API Endpoints

### Stories (/stories)
- GET /stories
- POST /stories
- PUT /stories/<id>
- DELETE /stories/<id>

### Pages & Choices
- POST /pages
- POST /pages/<id>/choices
- DELETE /choices/<id>
