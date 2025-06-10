from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from src.api.v1.api import api_router
from src.core.config import settings
from src.core.database import create_tables
from fastapi.responses import JSONResponse
from sqlalchemy.exc import OperationalError
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
    """Create PostgreSQL database tables on startup."""
    try:
        create_tables()
        print("PostgreSQL database initialized successfully")
    except OperationalError as e:
        print(f"PostgreSQL not available: {e}")
        print("⚠️  Please add PostgreSQL database to your deployment")
    except Exception as e:
        print(f"Database error: {e}")

# Include API routers
app.include_router(api_router, prefix="/api/v1")

@app.get("/")
def read_root():
    try:
        from src.core.database import engine
        with engine.connect():
            db_status = "✅ Connected"
    except:
        db_status = "❌ Not connected - Add PostgreSQL database"
    
    return {
        "message": "Welcome to the Smart Event Planner API",
        "docs": "/docs",
        "frontend": "/static/index.html",
        "version": "1.0.0",
        "status": "running",
        "database": db_status,
        "setup_required": "Add PostgreSQL database to your deployment platform"
    }

@app.get("/health")
def health_check():
    try:
        from src.core.database import engine
        with engine.connect() as conn:
            result = conn.execute("SELECT version()")
            pg_version = result.fetchone()[0]
        return {
            "status": "healthy",
            "service": "Smart Event Planner API",
            "database": {
                "type": "PostgreSQL",
                "status": "connected",
                "version": pg_version
            },
            "version": "1.0.0"
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "service": "Smart Event Planner API", 
            "database": {
                "type": "PostgreSQL",
                "status": "disconnected",
                "error": str(e)
            },
            "version": "1.0.0"
        }

@app.exception_handler(500)
async def internal_server_error_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error occurred"}
    )

@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    print(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={"detail": "An unexpected error occurred"}
    )

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