import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock
from sqlmodel import Session
from app.main import app
from app.database import get_session

@pytest.fixture
def mock_db():
    return MagicMock(spec=Session)

@pytest.fixture
def client(mock_db):
    app.dependency_overrides[get_session] = lambda: mock_db
    yield TestClient(app)
    app.dependency_overrides.clear()