from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_mock_gateway_success():

    response = client.post(
        "/mock/razorpay/auth"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["response"]["success"] is True
    assert data["response"]["status"] == "AUTHORIZED"