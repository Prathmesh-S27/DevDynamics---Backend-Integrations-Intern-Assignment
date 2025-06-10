from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pytest
from fastapi.testclient import TestClient
from src.main import app
from src.core.database import Base, get_db

@pytest.fixture(scope="session")
def db():
    engine = create_engine("postgresql://user:password@localhost/dbname")
    Base.metadata.create_all(bind=engine)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    yield db
    db.close()

@pytest.fixture(scope="module")
def test_client():
    with TestClient(app) as client:
        yield client

@pytest.fixture(scope="function")
def override_get_db(db):
    yield db

app.dependency_overrides[get_db] = override_get_db