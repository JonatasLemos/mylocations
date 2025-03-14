# flake8: noqa
from unittest.mock import MagicMock, call

import pytest
from api.utils.helpers import order_objects_with_literals  # Adjust the import path
from sqlalchemy.orm import Query
from sqlalchemy.sql.expression import literal_column


@pytest.fixture
def mock_query():
    """Fixture to return a mock SQLAlchemy query object."""
    return MagicMock(spec=Query)


def test_order_objects_with_literals_ascending(mock_query):
    """Test ordering in ascending order."""
    order_by_column = "created_at"

    result = order_objects_with_literals(order_by_column, "asc", mock_query)

    # Get the actual argument passed to order_by
    order_by_arg = mock_query.order_by.call_args[0][0]

    # Ensure it matches the expected column order
    assert str(order_by_arg) == str(literal_column(order_by_column))
    assert result == mock_query.order_by.return_value


def test_order_objects_with_literals_descending(mock_query):
    """Test ordering in descending order."""
    order_by_column = "name"

    result = order_objects_with_literals(order_by_column, "desc", mock_query)

    # Get the actual argument passed to order_by
    order_by_arg = mock_query.order_by.call_args[0][0]

    # Ensure it matches the expected column order in descending order
    assert str(order_by_arg) == str(literal_column(order_by_column).desc())
    assert result == mock_query.order_by.return_value


def test_order_objects_with_literals_case_insensitivity(mock_query):
    """Test case insensitivity of the order_param."""
    order_by_column = "updated_at"

    result = order_objects_with_literals(order_by_column, "DESC", mock_query)

    order_by_arg = mock_query.order_by.call_args[0][0]

    assert str(order_by_arg) == str(literal_column(order_by_column).desc())
    assert result == mock_query.order_by.return_value
