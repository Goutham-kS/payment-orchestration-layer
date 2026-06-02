from fastapi import APIRouter, Request, HTTPException

from app.core.gateway_router import GatewayRouter

router = APIRouter(
    prefix="/mock",
    tags=["Mock Gateways"]
)


@router.post("/{gateway}/auth")
async def mock_auth(
    gateway: str,
    request: Request
):

    headers = request.headers

    try:

        router_service = GatewayRouter()

        gateway_instance = router_service.get_gateway(gateway)

        result = await gateway_instance.authorize(
            amount=1000,
            headers=headers
        )

        return {
            "gateway": gateway,
            "operation": "AUTH",
            "response": result
        }

    except KeyError:
        raise HTTPException(
            status_code=404,
            detail=f"Gateway '{gateway}' not found"
        )


@router.post("/{gateway}/capture")
async def mock_capture(
    gateway: str,
    request: Request
):

    headers = request.headers

    try:

        router_service = GatewayRouter()

        gateway_instance = router_service.get_gateway(gateway)

        result = await gateway_instance.capture(
            transaction_id="mock_txn_123",
            headers=headers
        )

        return {
            "gateway": gateway,
            "operation": "CAPTURE",
            "response": result
        }

    except KeyError:
        raise HTTPException(
            status_code=404,
            detail=f"Gateway '{gateway}' not found"
        )