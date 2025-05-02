from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from starlette.responses import JSONResponse

from src.shared.infrastructure.database import close_db, init_db
from src.shared.infrastructure.routes_manager import RoutesManager

app = FastAPI(
    title="User Service API",
    description="API for managing users in the system.",
    version="1.0.0",
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
    print("Starting up User Service application...")
    # Initialize database connection and potentially create tables
    await init_db()
    print("Application startup complete.")


@app.on_event("shutdown")
async def shutdown_event():
    print("Shutting down User Service application...")
    # Close database connections gracefully
    await close_db()
    print("Application shutdown complete.")


# --- Exception Handlers ---
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    # Custom handler for Pydantic validation errors
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": exc.errors(), "body": exc.body},
    )


# --- Root Endpoint ---
@app.get("/", include_in_schema=False)
async def redirect_to_docs():
    return RedirectResponse(url="/docs")


routes_manager = RoutesManager(app)
routes_manager.include_router()
