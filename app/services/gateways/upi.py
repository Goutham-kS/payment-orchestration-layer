from app.services.gateways.base import PaymentGateway
from app.services.mock_gateway_service import simulate_gateway_response


class UPIGateway(PaymentGateway):

    async def authorize(self, amount: int, headers: dict):

        result = await simulate_gateway_response(headers)

        response_type = headers.get("X-UPI-Status", "SUCCESS")

        if response_type == "PENDING":
            result["status"] = "PENDING"

        elif response_type == "FAILED":
            result["status"] = "FAILED"

        elif response_type == "EXPIRED":
            result["status"] = "EXPIRED"

        else:
            result["status"] = "SUCCESS"

        result["payment_method"] = "UPI"

        return result

    async def capture(self, transaction_id: str, headers: dict):

        result = await simulate_gateway_response(headers)

        result["status"] = "CAPTURED"

        result["payment_method"] = "UPI"

        return result