from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from src.api.v1.api import api_router
from src.core.config import settings
from src.core.database import create_tables
import os

app = FastAPI(
    title="Smart Event Planner API", 
    version="1.0.0",
    description="A comprehensive weather-aware event planning system",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files for the frontend
try:
    app.mount("/static", StaticFiles(directory="src/static"), name="static")
except RuntimeError:
    # Handle case where static directory doesn't exist in some deployments
    pass

@app.on_event("startup")
async def startup_event():
    """Create database tables on startup."""
    try:
        create_tables()
        print("Database tables created successfully")
    except Exception as e:
        print(f"Database initialization error: {e}")

# Include API routers
app.include_router(api_router, prefix="/api/v1")

@app.get("/")
def read_root():
    return {
        "message": "Welcome to the Smart Event Planner API",
        "docs": "/docs",
        "frontend": "/static/index.html" if os.path.exists("src/static/index.html") else None,
        "version": "1.0.0",
        "status": "running"
    }

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "Smart Event Planner API"}

# For local development and deployment
if __name__ == "__main__":
    import uvicorn
    try:
        port = int(os.getenv("PORT", 8000))
        if port < 1 or port > 65535:
            port = 8000
    except (ValueError, TypeError):
        port = 8000
    
    uvicorn.run("src.main:app", host="0.0.0.0", port=port, reload=settings.DEBUG)