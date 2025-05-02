# Hexagonal Python Backend (FastAPI + CQRS)

[![Python 3.x](https://img.shields.io/badge/Python-3.x-blue)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/Framework-FastAPI-green)](https://fastapi.tiangolo.com/)
[![SQLAlchemy](https://img.shields.io/badge/ORM-SQLAlchemy-red)](https://www.sqlalchemy.org/)
[![RabbitMQ](https://img.shields.io/badge/Message_RabbitMQ-FF6600)](https://www.rabbitmq.com/)
[![uv](https://img.shields.io/badge/uv-0.1.16-blue)](https://github.com/astral-sh/uv)
[![pytest](https://img.shields.io/badge/pytest-8.2.2-blue)](https://docs.pytest.org/en/stable/)
[![Sphinx](https://img.shields.io/badge/Sphinx-7.3.7-blue)](https://www.sphinx-doc.org/en/master/)

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
docs/ # Project documentation source files
```


## 🚀 Features

- **Hexagonal Architecture**: Decoupled domain logic from frameworks.
- **CQRS**: Separate paths for:
  - **Commands**: `CreateUserCommand` (async via RabbitMQ)
  - **Queries**: `GetUserByIdQuery` (direct read)
- **Modular Design**: Isolated `users` and `auth` contexts.
- **Security**: Password hashing with BCrypt.
- **Fast Dependency Management**: Using `uv`.

## ⚙️ Setup

### Prerequisites
- Python 3.x
- Docker + Docker Compose
- `uv` (Python package installer and resolver)

### Installation
1. Clone the repository:
   ```bash
   git clone [your-repo-url]
   cd [your-repo-directory]
   ```
2. Create and activate a virtual environment (optional but recommended):
   ```bash
   python -m venv .venv
   # On Windows
   .\.venv\Scripts\activate
   # On macOS/Linux
   source .venv/bin/activate
   ```
3. Install dependencies using `uv`:
    ```bash
    uv sync
    ```
4. Start required services (PostgreSQL, RabbitMQ):
    ```bash
    docker-compose up -d
    ```

### Running the App
Start the FastAPI application using `uvicorn` managed by `uv`:
```bash
uv run uvicorn src.main:app --reload
```
The application will be available at `http://127.0.0.1:8000`.

## 🧪 Testing
Run tests using `pytest` managed by `uv`:
```bash
uv run pytest
```
To run tests with coverage:
```bash
uv run pytest --cov=src
```
**Goal**: 80%+ coverage.

## 📚 Documentation
The project documentation is built using Sphinx.

1. Activate your virtual environment:
   ```bash
   # On Windows
   .\.venv\Scripts\activate
   # On macOS/Linux
   source .venv/bin/activate
   ```
2. Navigate to the docs directory:
   ```bash
   cd docs
   ```
3. Build the HTML documentation:
   ```bash
   make html
   ```
The generated documentation can be found in the `docs/_build/html` directory. Open `index.html` in your browser.

## 🌐 API Endpoints

| Endpoint      | Method | Description                   |
|---------------|--------|-------------------------------|
| `/users`      | POST   | Create user (async command)   |
| `/users/{id}` | GET    | Get user by ID (direct query) |
| `/docs`       | GET    | API Documentation (Swagger UI)|
| `/redoc`      | GET    | API Documentation (ReDoc)     |

## 📜 Architectural Decisions
- Why Hexagonal?
Ensures business logic remains independent of databases/frameworks.

- Why CQRS?
Optimizes read/write scalability (RabbitMQ handles writes).

- Why Bundle-Contexts?
Encapsulates features (users/auth) for maintainability.

- Why `uv`?
Provides significantly faster dependency management compared to pip.
