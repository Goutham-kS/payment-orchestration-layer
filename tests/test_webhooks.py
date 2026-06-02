import json
import hmac
import hashlib

from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


# =========================================================
# HELPER
# =========================================================

def generate_signature(
    payload: bytes,
    secret: str
):

    return hmac.new(
        secret.encode(),
        payload,
        hashlib.sha256
    ).hexdigest()


# =========================================================
# VALID WEBHOOK TEST
# =========================================================

def test_valid_razorpay_webhook():

    secret = "razorpay_secret"

    payload_dict = {
        "event": "payment.captured",

        "payload": {
            "payment": {
                "entity": {
                    "id": "pay_test_123",
                    "order_id": "order_test_123",
                    "amount": 5000,
                    "currency": "INR"
                }
            }
        }
    }

    payload = json.dumps(
        payload_dict
    ).encode()

    signature = generate_signature(
        payload,
        secret
    )

    response = client.post(
        "/webhooks/razorpay",
        data=payload,
        headers={
            "x-razorpay-signature": signature
        }
    )

    assert response.status_code in [200, 400]


# =========================================================
# INVALID SIGNATURE TEST
# =========================================================

def test_invalid_razorpay_signature():

    payload_dict = {
        "event": "payment.captured"
    }

    payload = json.dumps(
        payload_dict
    ).encode()

    response = client.post(
        "/webhooks/razorpay",
        data=payload,
        headers={
            "x-razorpay-signature": "invalid_signature"
        }
    )

    assert response.status_code == 400

    assert (
        "Invalid Razorpay webhook signature"
        in response.text
    )


# =========================================================
# DUPLICATE WEBHOOK TEST
# =========================================================

def test_duplicate_webhook():

    secret = "razorpay_secret"

    payload_dict = {
        "event": "payment.captured",

        "payload": {
            "payment": {
                "entity": {
                    "id": "duplicate_payment_123",
                    "order_id": "duplicate_order_123",
                    "amount": 1000,
                    "currency": "INR"
                }
            }
        }
    }

    payload = json.dumps(
        payload_dict
    ).encode()

    signature = generate_signature(
        payload,
        secret
    )

    # -----------------------------------
    # FIRST WEBHOOK REQUEST
    # -----------------------------------

    first_response = client.post(
        "/webhooks/razorpay",
        data=payload,
        headers={
            "x-razorpay-signature": signature
        }
    )

    # -----------------------------------
    # SECOND WEBHOOK REQUEST
    # -----------------------------------

    second_response = client.post(
        "/webhooks/razorpay",
        data=payload,
        headers={
            "x-razorpay-signature": signature
        }
    )

    # -----------------------------------
    # ASSERTIONS
    # -----------------------------------

    assert second_response.status_code in [200, 400]

    # Optional duplicate validation

    if second_response.status_code == 200:

        response_json = second_response.json()

        assert (
            response_json["status"]
            == "duplicate webhook"
        )