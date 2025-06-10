from pydantic_settings import BaseSettings
import os

class Settings(BaseSettings):
    # Database - Use production DATABASE_URL if available
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://user:password@localhost/event_planner")
    
    # Security
    SECRET_KEY: str = "fallback-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Weather API
    OPENWEATHER_API_KEY: str = ""
    
    # Application
    DEBUG: bool = False  # Default to False for production
    ALLOW_ORIGINS: list = ["*"]
    
    # Email (Optional - for notifications)
    SMTP_EMAIL: str = "noreply@eventplanner.com"
    SMTP_PASSWORD: str = ""
    SMTP_SERVER: str = "smtp.gmail.com"
    SMTP_PORT: int = 587
    
    # Port configuration
    PORT: int = 8000

    class Config:
        env_file = ".env"
        
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Handle production PORT environment variable
        if os.getenv("PORT"):
            try:
                self.PORT = int(os.getenv("PORT"))
            except (ValueError, TypeError):
                self.PORT = 8000
        
        # Set DEBUG based on environment
        if os.getenv("DEBUG"):
            self.DEBUG = os.getenv("DEBUG").lower() in ("true", "1", "yes")

settings = Settings()