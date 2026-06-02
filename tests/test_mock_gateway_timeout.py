import time

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_mock_gateway_timeout():

    start = time.time()

    response = client.post(
        "/mock/razorpay/auth",
        headers={
            "X-Mock-Response": "timeout"
        }
    )

    end = time.time()

    assert end - start >= 35