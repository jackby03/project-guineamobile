from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse

from shared.infrastructure.routes.routes_manager import RoutesManager

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


@app.get("/", include_in_schema=False)
async def redirect_to_docs():
    """
    Redirect to the API documentation page.
    """
    return RedirectResponse(url="/docs")


routes_manager = RoutesManager(app)
routes_manager.include_router()
