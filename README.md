# Hexagonal Python Backend (FastAPI + CQRS)

[![Python 3.x](https://img.shields.io/badge/Python-3.x-blue)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/Framework-FastAPI-green)](https://fastapi.tiangolo.com/)
[![SQLAlchemy](https://img.shields.io/badge/ORM-SQLAlchemy-red)](https://www.sqlalchemy.org/)
[![RabbitMQ](https://img.shields.io/badge/Message_RabbitMQ-FF6600)](https://www.rabbitmq.com/)

A Python backend service implementing **Hexagonal Architecture** and **CQRS** pattern, with modular `bundle-contexts` for users and authentication.

## 📦 Project Structure
```
src/
├── contexts/
│ ├── users/
│ │ ├── domain/ # Entities, value objects, ports
│ │ ├── application/ # Use cases, commands, queries
│ │ └── infrastructure/ # Adapters (DB, API)
│ └── auth/ # Same structure as users
├── config/ # Dependency injection setup
└── tests/ # Unit and integration tests
```


## 🚀 Features

- **Hexagonal Architecture**: Decoupled domain logic from frameworks.
- **CQRS**: Separate paths for:
  - **Commands**: `CreateUserCommand` (async via RabbitMQ)
  - **Queries**: `GetUserByIdQuery` (direct read)
- **Modular Design**: Isolated `users` and `auth` contexts.
- **Security**: Password hashing with BCrypt.

## ⚙️ Setup

### Prerequisites
- Python 3.x
- Docker + Docker Compose

### Installation
1. Clone the repository:
   ```bash
   git clone [your-repo-url]
   ```
2. Start services:
    ```bash
    docker-compose up -d  # Launches PostgreSQL, RabbitMQ
    ```
3. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

### Running the App
```bash
flask dev src/app.py
```

## 🧪 Testing
Run tests with coverage:
```bash
pytest --cov=src/contexts/users/domain
```
**Goal**: 80%+ coverage in domain layer.

## 🌐 API Endpoints

| Endpoint        | Method | Description                     |
|----------------|--------|---------------------------------|
| `/users`       | POST   | Create user (async command)     |
| `/users/{id}`  | GET    | Get user by ID (direct query)   |

## 📜 Architectural Decisions
- Why Hexagonal?
Ensures business logic remains independent of databases/frameworks.

- Why CQRS?
Optimizes read/write scalability (RabbitMQ handles writes).

- Why Bundle-Contexts?
Encapsulates features (users/auth) for maintainability.

