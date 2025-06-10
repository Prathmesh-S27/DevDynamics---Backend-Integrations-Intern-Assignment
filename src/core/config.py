from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    OPENWEATHER_API_KEY: str
    ALLOW_ORIGINS: list = ["*"]
    
    # Email settings for notifications
    SMTP_EMAIL: str = "noreply@eventplanner.com"
    SMTP_PASSWORD: str = ""
    SMTP_SERVER: str = "smtp.gmail.com"
    SMTP_PORT: int = 587

    class Config:
        env_file = ".env"

settings = Settings()