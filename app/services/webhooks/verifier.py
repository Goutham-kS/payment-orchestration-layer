import hmac
import hashlib


# =========================================================
# GENERIC HMAC SIGNATURE VERIFIER
# =========================================================

def verify_hmac_signature(
    payload: bytes,
    signature: str,
    secret: str
) -> bool:

    expected_signature = hmac.new(
        secret.encode(),
        payload,
        hashlib.sha256
    ).hexdigest()

    return hmac.compare_digest(
        expected_signature,
        signature
    )


# =========================================================
# RAZORPAY SIGNATURE VERIFICATION
# =========================================================

def verify_razorpay_signature(
    payload: bytes,
    signature: str,
    secret: str
) -> bool:

    return verify_hmac_signature(
        payload=payload,
        signature=signature,
        secret=secret
    )


# =========================================================
# STRIPE SIGNATURE VERIFICATION
# =========================================================

def verify_stripe_signature(
    payload: bytes,
    signature: str,
    secret: str
) -> bool:

    return verify_hmac_signature(
        payload=payload,
        signature=signature,
        secret=secret
    )


# =========================================================
# GENERATE PAYLOAD HASH
# =========================================================

def generate_payload_hash(
    payload: bytes
) -> str:

    return hashlib.sha256(
        payload
    ).hexdigest()