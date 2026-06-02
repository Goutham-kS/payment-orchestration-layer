from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_mock_gateway_decline():

    response = client.post(
        "/mock/razorpay/auth",
        headers={
            "X-Mock-Response": "decline"
        }
    )

    assert response.status_code == 402