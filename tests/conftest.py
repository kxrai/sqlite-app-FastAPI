import pytest
from fastapi.testclient import TestClient
from app.main import app

@pytest.fixture(scope="module")
def test_client():
    """
    Fixture to create a TestClient for the FastAPI app.
    This client will be used in the tests to make requests to the API.
    """
    client = TestClient(app)
    yield client
