import asyncio
import uuid

from fastapi import HTTPException

from app.core.exceptions import (
    GatewayTimeoutError,
    GatewayFailedError,
)


# ==========================================
# COMMON MOCK RESPONSE SIMULATOR
# ==========================================

async def simulate_gateway_response(
    headers: dict
):

    # Read mock headers

    response_type = headers.get(
        "X-Mock-Response",
        "success"
    )

    delay_ms = headers.get(
        "X-Mock-Delay-Ms",
        "0"
    )

    gateway_down = headers.get(
        "X-Mock-Gateway-Down",
        "false"
    )

    # Convert delay safely

    try:
        delay_ms = int(delay_ms)

    except ValueError:
        delay_ms = 0

    # ==========================================
    # Artificial network delay
    # ==========================================

    if delay_ms > 0:

        await asyncio.sleep(
            delay_ms / 1000
        )

    # ==========================================
    # Gateway completely down
    # ==========================================

    if gateway_down.lower() == "true":

        raise HTTPException(
            status_code=503,
            detail={
                "success": False,
                "error": "Gateway Down"
            }
        )

    # ==========================================
    # Timeout simulation
    # ==========================================

    if response_type == "timeout":

        await asyncio.sleep(2)

        raise GatewayTimeoutError(
            "Gateway timeout"
        )

    # ==========================================
    # 5xx server error simulation
    # ==========================================

    if response_type == "server-error":

        raise GatewayFailedError(
            "Gateway server error"
        )

    # ==========================================
    # Payment decline simulation
    # ==========================================

    if response_type == "decline":

        raise HTTPException(
            status_code=402,
            detail={
                "success": False,
                "error": "Payment Declined",
                "reason": "Insufficient funds"
            }
        )

    # ==========================================
    # Rate limiting simulation
    # ==========================================

    if response_type == "rate-limit":

        raise HTTPException(
            status_code=429,
            detail={
                "success": False,
                "error": "Rate Limit Exceeded"
            },
            headers={
                "Retry-After": "5"
            }
        )

    # ==========================================
    # Default success response
    # ==========================================

    await asyncio.sleep(1)

    return {
        "success": True,
        "gateway_transaction_id":
            f"mock_txn_{uuid.uuid4().hex[:10]}",
        "status": "AUTHORIZED",
        "message":
            "Payment authorized successfully"
    }


# ==========================================
# RAZORPAY MOCK
# ==========================================

async def process_razorpay_payment(
    headers: dict = {}
):

    response = await simulate_gateway_response(
        headers
    )

    response["gateway"] = "razorpay"

    return response


# ==========================================
# STRIPE MOCK
# ==========================================

async def process_stripe_payment(
    headers: dict = {}
):

    response = await simulate_gateway_response(
        headers
    )

    response["gateway"] = "stripe"

    return response