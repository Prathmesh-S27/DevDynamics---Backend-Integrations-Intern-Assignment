from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from src.api.v1.api import api_router
from src.core.config import settings
from src.core.database import create_tables

app = FastAPI(title="Smart Event Planner API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOW_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files for the frontend
app.mount("/static", StaticFiles(directory="src/static"), name="static")

@app.on_event("startup")
async def startup_event():
    """Create database tables on startup."""
    create_tables()

app.include_router(api_router, prefix="/api/v1")

@app.get("/")
def read_root():
    return {"message": "Welcome to the Smart Event Planner API", "dashboard": "/static/index.html"}