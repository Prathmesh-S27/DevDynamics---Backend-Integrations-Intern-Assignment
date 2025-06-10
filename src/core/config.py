from pydantic_settings import BaseSettings
import os

class Settings(BaseSettings):
    # Database
    DATABASE_URL: str = "postgresql://user:password@localhost/event_planner"
    
    # Security
    SECRET_KEY: str = "fallback-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Weather API
    OPENWEATHER_API_KEY: str = ""
    
    # Application
    DEBUG: bool = True
    ALLOW_ORIGINS: list = ["*"]
    
    # Email (Optional - for notifications)
    SMTP_EMAIL: str = "noreply@eventplanner.com"
    SMTP_PASSWORD: str = ""
    SMTP_SERVER: str = "smtp.gmail.com"
    SMTP_PORT: int = 587
    
    # Render specific
    PORT: int = 8000

    class Config:
        env_file = ".env"
        
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Handle Render's PORT environment variable
        if os.getenv("PORT"):
            self.PORT = int(os.getenv("PORT"))

settings = Settings()