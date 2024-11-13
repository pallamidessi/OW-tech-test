# Import sys module for modifying Python's runtime environment
import sys

# Import os module for interacting with the operating system
import os

# Add the parent directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import the Flask app instance from the main app file
from main import app

# Import pytest for writing and running tests
import pytest
from unittest.mock import patch


@pytest.fixture
def client():
    """A test client for the app."""
    with app.test_client() as client:
        yield client


def test_home(client):
    """Test the home route."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json == {"message": "Hello, Flask!"}

# Here we are testing the full endpoint and mocking the API calls
@patch("main.get_current_billing_period")
@patch("main.get_report")
def test_usage(mock_get_report, mock_get_current_billing_period, client):
    """Test the usage route."""
    mock_get_current_billing_period.return_value = {
        "messages": [
            {
                "text": "Generate a Tenant Obligations Report for the new lease terms.",
                "timestamp": "2024-04-29T02:08:29.375Z",
                "report_id": 5392,
                "id": 1000,
            },
            {
                "text": "Are there any restrictions on alterations or improvements?",
                "timestamp": "2024-04-29T03:25:03.613Z",
                "id": 1001,
            },
            {
                "text": "Is there a clause for default and remedies?",
                "timestamp": "2024-04-29T07:27:34.985Z",
                "id": 1002,
            },
        ]
    }

    mock_get_report.return_value = {
        "id": 5392,
        "name": "Retail Lease Report",
        "credit_cost": 79,
    }

    response = client.get("/usage")
    print(response.json)
    assert response.status_code == 200
    assert response.json == {
        "usage": [
            {
                "credit_used": 79,
                "message_id": 1000,
                "report_name": 5392,
                "timestamp": "2024-04-29T02:08:29.375Z",
            },
            {
                "credit_used": 6.1,
                "message_id": 1001,
                "timestamp": "2024-04-29T03:25:03.613Z",
            },
            {
                "credit_used": 3.65,
                "message_id": 1002,
                "timestamp": "2024-04-29T07:27:34.985Z",
            },
        ]
    }
