# Mini Uber Eats

A food delivery platform inspired by Uber Eats, built with Django REST Framework on the backend and React + Vite on the frontend. The project includes customer ordering, restaurant management, driver delivery workflows, real-time order tracking, and Docker-based local setup.

## Tech Stack

- Backend: Python, Django, Django REST Framework, JWT Auth
- Frontend: React, Vite, Tailwind CSS
- Database: PostgreSQL
- Cache / Queue: Redis
- Background Jobs: Celery
- Mail Testing: Mailpit
- Containerization: Docker + Docker Compose

## Features

- Customer account registration and login
- Restaurant listing and menu browsing
- Cart and checkout flow
- Order placement and payment confirmation flow
- Restaurant owner dashboard for accepting and managing orders
- Driver dashboard for available orders and delivery states
- Mail notifications via Mailpit
- Dockerized local environment for easy onboarding

## Project Structure

```bash
.
├── backend/
│   ├── carts/
│   ├── config/
│   ├── delivery/
│   ├── menus/
│   ├── notifications/
│   ├── orders/
│   ├── payments/
│   ├── restaurants/
│   ├── users/
│   ├── manage.py
│   └── requirements.txt
├── frontend/
│   ├── src/
│   ├── package.json
│   ├── vite.config.js
│   └── index.html
├── docker-compose.yml
├── .env
├── .env.example
├── .gitignore
└── README.md
```

## Prerequisites

Before running the project, install:

- Docker
- Docker Compose

## Environment Setup

Copy the example environment file if needed:

```bash
cp .env.example .env
```

Then update the values in `.env` as required. The project already includes the default local development variables for Docker-based setup.

## Run the Project

From the project root:

```bash
docker compose up --build
```

This will start:

- Frontend: http://localhost:5173
- Backend API: http://localhost:8000
- Mailpit UI: http://localhost:8025
- Flower UI: http://localhost:5555
- PostgreSQL: localhost:5432
- Redis: localhost:6379

## Useful Commands

### Start services

```bash
docker compose up
```

### Stop services

```bash
docker compose down
```

### Rebuild containers after dependency or config changes

```bash
docker compose up --build
```

### Run backend migrations

```bash
docker compose run --rm backend python manage.py migrate
```

### Create a Django superuser

```bash
docker compose run --rm backend python manage.py createsuperuser
```

### Run backend tests

```bash
docker compose run --rm backend python manage.py test
```

### Access the backend shell

```bash
docker compose run --rm backend python manage.py shell
```

## Default Roles

The app supports these user roles:

- CUSTOMER
- RESTAURANT_OWNER
- DRIVER
- ADMIN

## Notes

- Mailpit is configured for local email testing and can be accessed through the Mailpit web UI on port 8025.
- The frontend uses a Tailwind-based design system and is optimized for a modern food delivery experience.
- Redis and Celery handle background tasks such as notifications, cart cleanup, and delivery processing.

