# flake8: noqa
from unittest.mock import MagicMock, patch

import pytest
from core.database import get_db
from fastapi.testclient import TestClient
from jose import jwt
from main import app
from models.user import User
from schemas.location_schema import LocationTypeOut


client = TestClient(app)
mock_session = MagicMock()

app.dependency_overrides[get_db] = lambda: mock_session


@pytest.fixture
def mock_user():
    """Fixture to return a mock authenticated user."""
    return User(id=1, username="testuser")


@pytest.fixture
def mock_jwt():
    """Fixture to return mock JWT payload."""
    return {"sub": "testuser"}


@pytest.fixture
def mock_location_types():
    """Fixture to return mock location types."""
    return [
        LocationTypeOut(id=1, name="Type 1", created_at=None),
        LocationTypeOut(id=2, name="Type 2", created_at=None),
    ]


@pytest.fixture
def patch_dependencies(mock_user, mock_jwt):
    """Fixture to patch common dependencies."""
    with (
        patch("core.database.get_db", return_value=mock_session),
        patch("api.utils.security.validate_token", return_value=mock_user),
        patch("jose.jwt.decode", return_value=mock_jwt),
    ):
        yield


def test_list_location_types_mock(patch_dependencies, mock_location_types):
    """Test listing location types with mocked DB session."""

    # Mock paginated data
    mock_session.query.return_value.count.return_value = len(mock_location_types)
    mock_session.query.return_value.offset.return_value.limit.return_value.all.return_value = (
        mock_location_types
    )

    response = client.get(
        "/location-types/list/?page=1&size=10",
        headers={"Authorization": "Bearer mock_token"},
    )

    # Validate response
    assert response.status_code == 200
    assert response.json() == {
        "items": [location.model_dump() for location in mock_location_types],
        "total": len(mock_location_types),
        "page": 1,
        "size": 10,
        "pages": 1,
    }


def test_detail_location_type_mock(patch_dependencies):
    """Test fetching a specific location type with mocked DB session."""

    mock_location_type = LocationTypeOut(id=1, name="Test Type", created_at=None)

    # Ensure querying User returns mock_user, and querying LocationType returns mock_location_type
    mock_session.query.return_value.filter.return_value.first.side_effect = [
        User(id=1, username="testuser"),  # First call (for authentication)
        mock_location_type,  # Second call (for fetching location type)
    ]

    # Perform the test request
    response = client.get(
        "/location-types/1/",
        headers={"Authorization": "Bearer mock_token"},
    )

    # Validate response
    assert response.status_code == 200
    assert response.json() == mock_location_type.model_dump()
