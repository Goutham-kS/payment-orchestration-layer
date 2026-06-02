from app.services.gateways.base import PaymentGateway
from app.services.mock_gateway_service import simulate_gateway_response


class PayUGateway(PaymentGateway):

    async def authorize(self, amount: int, headers: dict):
        return await simulate_gateway_response(headers)

    async def capture(self, transaction_id: str, headers: dict):
        return await simulate_gateway_response(headers)