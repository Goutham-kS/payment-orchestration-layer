from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_upi_expired():

    response = client.post(
        "/mock/upi/auth",
        headers={
            "X-UPI-Status": "EXPIRED"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["response"]["status"] == "EXPIRED"