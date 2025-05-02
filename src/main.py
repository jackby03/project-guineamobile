from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse

from shared.configuration.config import settings
from shared.infrastructure.messaging import close_rabbitmq_connection
from src.shared.infrastructure.database import close_db, init_db
from src.shared.infrastructure.routes_manager import RoutesManager

app = FastAPI(
    title="User Service API",
    description="API for managing users in the system.",
    version="1.0.0",
    docs_url="/docs" if settings.ENVIRONMENT == "development" else None,
    redoc_url="/redoc" if settings.ENVIRONMENT == "development" else None,
)

# configuration of CORS
# This allows cross-origin requests from any origin.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --- Event Handlers ---
@app.on_event("startup")
async def startup_event():
    """
    Startup event handler.

    This function is executed when the application starts. It initializes
    the database connection and performs any necessary setup.

    Returns:
        None
    """
    print("Starting up User Service application...")
    await init_db()
    print("Application startup complete.")


@app.on_event("shutdown")
async def shutdown_event():
    """
    Shutdown event handler.

    This function is executed when the application shuts down. It closes
    database connections and other resources gracefully.

    Returns:
        None
    """
    print("Shutting down User Service application...")
    await close_db()
    await close_rabbitmq_connection()
    print("Application shutdown complete.")


# --- Exception Handlers ---
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """
    Handle validation exceptions for FastAPI requests.

    This function serves as an exception handler for `RequestValidationError`,
    returning a JSON response with validation error details.

    Args:
        request (Request): The incoming HTTP request object.
        exc (RequestValidationError): The validation exception that was raised.

    Returns:
        JSONResponse: A response containing:
            - status_code: 422 (HTTP_422_UNPROCESSABLE_ENTITY).
            - content: Dictionary with 'detail' key containing validation errors.

    Example:
        When invalid data is sent:
        {
            "detail": [
                {
                    "loc": ["body", "email"],
                    "msg": "invalid email format",
                    "type": "value_error"
                }
            ]
        }
    """
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": exc.errors()},
    )


# --- Include Routers ---
routes_manager = RoutesManager(app)
routes_manager.include_router()


# --- Root Endpoint ---
@app.get("/", include_in_schema=False)
async def redirect_to_docs():
    """
    Root endpoint providing basic app info.

    This endpoint returns basic information about the application, including
    the environment, version, and documentation URL.

    Returns:
        dict: A dictionary containing app information.
    """
    return {
        "message": "Welcome to the User Service API!",
        "enviroment": settings.ENVIRONMENT,
        "version": app.version,
        "docs_url": app.docs_url,
    }
